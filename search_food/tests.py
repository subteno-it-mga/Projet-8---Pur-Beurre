'''
search_food/tests.py
This file tests every functions in the app.
'''
import json
from urllib.request import urlopen
import time
from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
import httpretty
import requests
from unidecode import unidecode
from selenium import webdriver
from .models import Product, User, Favorite, SubstituteProduct
from .views import call_api_for_product, create_entries, \
    display_informations, delete_all_entries, change_nutriscore, \
    display_substitutes, search_categories, add_substitute_products, \
    add_favorite_database

import random
import string
import os

TRAVIS_PROD = os.environ.get('TRAVIS_PROD')

if TRAVIS_PROD:
    test_url = TRAVIS_PROD
else:
    test_url = 'http://localhost:8000/'


class TestCallAPI(TestCase):
    '''
    This is the tests for the two API CALLS and functions in this app
    '''

    def setUp(self):
        '''
        Setting up the factory variable
        '''
        self.factory = RequestFactory()

    @httpretty.activate
    def test_call_api_for_product(self):
        '''
        Test this functionnality wich is use to call API, get the JSON then
        stock in database.
        In this function, we'll only test the API CALL.
        We'll use Httpretty to mock the http call to OpenFoodFact API.
        '''
        product = "Nutella"

        httpretty.enable()
        url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=%s" \
            "&action=process&json=1&page_size=1" \
            % (product)

        # Here test the response and integrity of information given.
        httpretty.register_uri(
            httpretty.GET, url,
            body='{"page_size": 20,"products":[{"product_name": "Nutella"}]}',
            content_type="application/json")

        response = requests.get(url)
        last_request = httpretty.last_request()

        self.assertEqual(last_request.method, 'GET')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"page_size": 20, "products": [
                {"product_name": "Nutella"}]})

        # Test if we can read the json file and retrieve good informations .
        result = urlopen(url)
        json_result = json.load(result)
        categ_product = json_result['products']

        self.assertEqual(categ_product[0]['product_name'], "Nutella")

        # Clean up the process
        httpretty.disable()
        httpretty.reset()

    @httpretty.activate
    def test_call_api_for_category(self):
        '''
        Test this functionnality wich is use to call API, get the JSON then
        stock in database.
        In this function, we'll only test the API CALL.
        We'll use Httpretty to mock the http call to OpenFoodFact API.
        '''
        category = "en:biscuîts"
        # Start httpretty process.
        httpretty.enable()
        category_clean = unidecode(category)

        self.assertEqual(category_clean, "en:biscuits")

        url = "https://world.openfoodfacts.org/cgi/search.pl?action=process" \
            "&tagtype_0=categories&tag_contains_0=" \
            "contains&tag_0=%s&page_size=100&axis_x=energy&axis_y=" \
            "products_n&action=display&json=1" % (category_clean)
        # Here test the response and integrity of information given.
        httpretty.register_uri(
            httpretty.GET, url,
            body='{"skip": 0,"page_size": 100,"products":'
            '[{"product_name_fr": "Prince: Goût Chocolat au Blé Complet"}]}',
            content_type="application/json")

        response = requests.get(url)
        last_request = httpretty.last_request()

        self.assertEqual(last_request.method, 'GET')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "skip": 0,
            "page_size": 100,
            "products": [{
                "product_name_fr": "Prince: Goût Chocolat au Blé Complet"}]})

        # Test if we can read the json file and retrieve good informations.
        result = urlopen(url)
        json_result = json.load(result)
        categ_product = json_result['products']

        self.assertEqual(categ_product[0]['product_name_fr'],
                         "Prince: Goût Chocolat au Blé Complet")

        # Clean up the process
        httpretty.disable()
        httpretty.reset()

    def test_treat_input_term(self):
        '''
        This function tests if the keyword(s) are split and if the api call is
        successful.
        '''
        test_keyword = unidecode("pains au chocôlat")

        # Check if the accentutation is removed or not
        self.assertEqual(test_keyword, 'pains au chocolat')

        test_list_term = test_keyword.split(" ")
        test_final_term_list = []

        for test_item in test_list_term:

            if test_list_term[len(test_list_term) - 1] == test_item:
                test_final_term_list.append(test_item)
            else:
                new_item = "".join(test_item + '%20')
                test_final_term_list.append(new_item)

        test_final_term_string = ''.join(test_final_term_list)

        test_product = call_api_for_product(test_final_term_string)

        create_entries(test_product, test_final_term_string)

        # informations_displayed = display_informations(final_term_string)

        # Test if the loop assemblate the term to search a product in the API.
        self.assertEqual(test_final_term_string, 'pains%20au%20chocolat')

        # Test if the value return the good data
        self.assertEqual(test_product[0]['product_name'], "Pains au chocolat")

        # Test if the product is in the database
        self.assertEqual(Product.objects.get(
            barcode=test_product[0]['code']).barcode, 3256540001008)

    def test_search_and_stock(self):
        '''
        This function tests if the route exists and return a 200 response.
        '''
        client = Client()
        response = client.post(
            reverse('search_and_stock'),
            {"search_term": "nutella"})
        self.assertTrue(response.status_code, 200)


class DatabaseTestCase(TestCase):
    '''
    Test for products in database
    '''

    def setUp(self):
        '''
        Setting up all objects for the test. All datas will be erase after the
        test
        '''
        # Create a test user in the database
        self.user_test = User.objects.create_user(
            'testuser', 'user@user.fr', 'passwordtest')

        # Create a product in the database
        self.product_test_generic = Product.objects.create(
            name='Nutella',
            description='testdescription',
            category='pâte à tartiner',
            fat=1,
            salt=1,
            image='nutella.jpg',
            sugar=1,
            nutriscore=4,
            barcode=123456789,
            search='nutella')

        self.product_test_generic.save()

        # Create a substitute from the product in the database
        self.product_substitute = SubstituteProduct.objects.create(
            name='gerblé',
            category='pâte à tartiner',
            description='testdescriptionsub',
            nutriscore=1,
            fat=1,
            sugar=1,
            salt=1,
            image='sub.jpg',
            barcode=12345678910,
            original=self.product_test_generic)

        # Create favorite datas from user and substitute
        self.user_favorite = Favorite.objects.create(
            product_name='gerblé_fav',
            barcode=1234567891011,
            product_associate=self.product_test_generic,
            user_associate=self.user_test)

        self.factory = RequestFactory()
        self.client = Client()
        self.search = 'nutella'

    def test_change_nutriscore(self):
        '''
        Test if the nutriscore is well substitute.
        '''
        # Test if the nutriscore change from strong to integer for a better
        # sort in the template
        test_change_nutriscore_a = change_nutriscore("a")
        test_change_nutriscore_b = change_nutriscore("b")
        test_change_nutriscore_c = change_nutriscore("c")
        test_change_nutriscore_d = change_nutriscore("d")
        test_change_nutriscore_e = change_nutriscore("e")

        test_change_nutriscore_x = change_nutriscore("x")

        self.assertEqual(test_change_nutriscore_a, 1)
        self.assertEqual(test_change_nutriscore_b, 2)
        self.assertEqual(test_change_nutriscore_c, 3)
        self.assertEqual(test_change_nutriscore_d, 4)
        self.assertEqual(test_change_nutriscore_e, 5)
        self.assertEqual(test_change_nutriscore_x, "Pas de Nutriscore.")

    def test_create_entries(self):
        '''
        Test the entries in the database. Then look if the entry exists or not.
        '''
        # Initialize a json file, a database object, then save entries in the
        # database.
        test_json_file = call_api_for_product("nutella")
        create_entries(test_json_file, "nutella")

        # Check if the products was saved in the database
        self.assertTrue(Product.objects.all().count(),
                        Product.objects.all().count() > 5)
        self.assertEqual(Product.objects.get(
            barcode=test_json_file[0]['code']).name, "Nutella")

        # Check if the entries in database are all unique by their barcodes.
        for product in Product.objects.all():
            print(product)
            self.assertEqual(Product.objects.filter(
                barcode=test_json_file[0]['code']).count(), 1)

    def test_delete_entries(self):
        '''
        Test if all entries are deleted well after calling the delete function.
        '''
        # Get the user by his username
        test_user_object = User.objects.get(username='testuser')

        # Call the function to delete all entries
        delete_all_entries()

        # Test if the user is not deleted when we're calling the function to
        # delete all entries
        self.assertEqual(test_user_object.username, 'testuser')

        # Test if the database is clean from product
        self.assertQuerysetEqual(
            SubstituteProduct.objects.filter(barcode=123456789), [])
        self.assertQuerysetEqual(
            SubstituteProduct.objects.filter(barcode=12345678910), [])
        self.assertQuerysetEqual(
            Favorite.objects.filter(barcode=1234567891011), [])

        # Check if we don't forget an entry in database so try to search any
        # data in database
        self.assertQuerysetEqual(Product.objects.all(), [])
        self.assertQuerysetEqual(SubstituteProduct.objects.all(), [])
        self.assertQuerysetEqual(Favorite.objects.all(), [])

        response = self.client.post(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'standard/index.html')
        self.assertContains(
            response,
            '<h1 class="text-white font-weight-bold">Du gras oui, mais de qualité !</h1>')

    def test_display_informations(self):
        '''
        Test if we retrieve correctly all products in database.
        '''
        test2_keyword = unidecode("nutella")
        test2_list_term = test2_keyword.split(" ")
        test2_final_term_list = []

        for test2_item in test2_list_term:

            if test2_list_term[len(test2_list_term) - 1] == test2_item:
                test2_final_term_list.append(test2_item)
            else:
                test2_new_item = "".join(test2_item + '%20')
                test2_final_term_list.append(test2_new_item)

        test2_final_term_string = ''.join(test2_final_term_list)

        # Call the function which is display all products in database
        test2_test_display = display_informations(test2_final_term_string)

        # Test if the function return a queryset of all product in database.
        self.assertQuerysetEqual(test2_test_display, ['<Product: Nutella>'])

    def test_display_substitutes(self):
        '''
        Test if the data are saved correctly in database.
        '''
        # Get the product registered before
        test_query_product = Product.objects.get(barcode=123456789)

        # Call the function wich display substitutes from the original product
        test_substitute_query = display_substitutes(test_query_product)

        # Test if the function return a correct queryset from the original
        # product
        self.assertQuerysetEqual(
            test_substitute_query,
            ['<SubstituteProduct: gerblé>'])

    def test_search_categories(self):
        '''
        Test the search categories function, depends on barcode
        '''
        # Get the product registered before
        test_query_product = Product.objects.get(barcode=123456789)

        # Two queries : one to trigger the good informaions and the other to
        # return an error
        test_search_category = search_categories(test_query_product.barcode)
        test_search_category_wrong = search_categories(10203040)

        # Check the values if we enter a good or a wrong barcode
        self.assertEqual(test_search_category, 'pâte à tartiner')
        self.assertEqual(test_search_category_wrong,
                         "Ce produit n'est pas ou plus présent dans la base.")

    def test_substitute_products(self):
        '''
        Test if the substitute are correctly saved in database
        '''
        # Get the product registered before
        test_original_product = Product.objects.get(barcode=123456789)

        test_data_dictionnary = {
            'product': 'gerblé2',
            'salt': 1,
            'sugar': 1,
            'fat': 1,
            'description': 'subtestdescription',
            'image': 'subtest.jpg',
            'nutriscore': 4,
            'barcode': 1234567891011,
            'category': 'pâte à tartiner',
            'original': test_original_product,
        }

        # Call this function to save substitute products in database
        add_substitute_products(test_data_dictionnary)

        # Retrieve the substitute from his barcode
        test_query_substitute = SubstituteProduct.objects.filter(
            barcode=1234567891011)

        # Test if he subsistute obect his created
        self.assertQuerysetEqual(
            test_query_substitute,
            ['<SubstituteProduct: gerblé2>'])

    def test_add_favorite_database(self):
        '''
        Test if the product are added as favorite in database.
        '''

        # We call the function to add a favorite in database with the
        # substitute product and the user in parameter
        add_favorite_database(self.product_substitute.barcode, self.user_test)

        # Test i we have all datas in the favorite database and if it's match
        # with the substitute define
        self.assertQuerysetEqual(Favorite.objects.filter(
            barcode=12345678910), ['<Favorite: gerblé>'])
        self.assertEqual(Favorite.objects.get(
            barcode=12345678910).user_associate.username, 'testuser')
        self.assertEqual(Favorite.objects.get(
            barcode=12345678910).product_name, 'gerblé')

    def test_display_favorite(self):
        '''
        Test if the favorite are display the correct way
        '''
        self.client.force_login(self.user_test)
        url = reverse('display_favorite')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'standard/favorite.html')
        self.assertContains(response, '<h1 style="color:white;">Favoris</h1>')

    def test_check_search(self):
        '''
        Test if the lower function works for the search input.
        '''
        test_true = Product.objects.filter(search=self.search.lower())
        test_false = Product.objects.filter(search="cacao")

        if test_true:
            self.assertTrue(test_true)
        else:
            self.assertFalse(test_false)

    def test_add_favorite(self):
        '''
        Test the add to favorite.
        '''
        client = Client()
        client.login(username='testuser', password='passwordtest')
        response = client.post(
            reverse('add_favorite'), {'barcode': 12345678910})
        self.assertTrue(response.status_code, 200)


class TestBasicViews(TestCase):
    '''
    This class tests basic views
    '''

    def test_home_page_status_code(self):
        '''
        Check if the returned status code of the page is 200
        '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        '''
        Check if the url returned is good
        '''
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        '''
        Test if we use the correct template and it returns a 200 status_code
        '''
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'standard/index.html')

    def test_home_page_contains_correct_html(self):
        '''
        Test if the html page contains the h1 title (only present in the index
        page)
        '''
        response = self.client.get('/')
        self.assertContains(
            response, '<h1 class="text-white font-weight-bold">Du gras oui, mais de qualité !</h1>')

    def test_home_page_does_not_contain_incorrect_html(self):
        '''
        Test if the page doesn't contain bad html
        '''
        response = self.client.get('/')
        self.assertNotContains(response, 'That\'s incorrect html')


class TestUserAccount(TestCase):
    '''
    This class test the UserAccount functionalities.
    '''
    # pylint: disable=too-many-instance-attributes
    # Reasonable in this case, i can't split function or put it in other class.
    def setUp(self):
        '''
        Setting up the class with some useful variables.
        '''
        self.client = Client()
        self.client1 = Client()
        self.client2 = Client()
        self.client3 = Client()
        self.client4 = Client()

        self.user_form = {
            'username': 'jacques',
            'password1': 'jaja61700',
            'password2': 'jaja61700'
        }
        self.user = UserCreationForm(self.user_form)
        self.user.save()
        self.factory = RequestFactory()

        self.response_true = self.client1.post(
            reverse('user_account'),
            {'username': 'jacques', 'password': 'jaja61700'})

        self.response_false = self.client2.post(
            reverse('user_account'),
            {'username': 'jacques', 'password': 'jaja'})

        self.test_form2 = UserCreationForm({
            'username': "martinbg61",
            'password1': "calvadosdedans61",
            'password2': "calvadosdedans61"
        })

    def test_logout_user(self):
        '''
        Test if the logout works well.
        '''
        self.client.login(username='jacques', password='jaja61700')
        response = self.client.get(reverse('logout_user'))

        self.assertEqual(response.status_code, 302)

    def test_user_account(self):
        '''
        Test few case where the user logged in.
        '''
        self.assertEqual(self.response_true.status_code, 200)

        self.assertEqual(self.response_false.status_code, 200)

        self.assertTrue(self.test_form2.is_valid())
        if self.test_form2.is_valid():

            self.test_form2.save()
            response = self.client4.get(reverse('signup'))
            self.assertEqual(response.status_code, 200)

    def test_post_user_creation_case_wrong(self):
        '''
        Check if the form is False when the user doesn't fill one or few
        informations.
        '''
        # Test : Empty Username
        form_data_no_user = {
            "username": "",
            "password1": "vitamineD61",
            "password2": "vitamineD61",
            "info": "empty no username"}

        # Test : two passwords doesn't matches
        form_data_no_matching_pwd = {
            "username": "martin",
            "password1": "matchingpass",
            "password2": "matching",
            "info": "no matching pwd"}

        # Test : empty passwords fields
        form_data_no_pwd = {
            "username": "martin",
            "password1": "",
            "password2": "",
            "info": "empty password"}

        # Test : weak passwords (rule : more than 8 characters)
        form_data_weak_password = {
            "username": "martin",
            "password1": "weak",
            "password2": "weak",
            "info": "weak password"}

        test_list_user_creation = [
            form_data_no_user,
            form_data_no_matching_pwd,
            form_data_no_pwd,
            form_data_weak_password]

        for test_user_creation in test_list_user_creation:
            form = UserCreationForm(data=test_user_creation)
            if form.is_valid():
                pass
            else:
                self.assertFalse(form.is_valid())

    def test_login_user(self):
        '''
        Test if the user login works.
        '''
        client1 = Client()
        client2 = Client()

        response_true = client1.post(
            reverse('login_user'),
            {'username': 'jacques', 'password': 'jaja61700'})
        self.assertEqual(response_true.status_code, 302)

        response_false = client2.post(
            reverse('login_user'),
            {'username': 'ja', 'password': 'jaja61700'})
        self.assertTrue(response_false.status_code, 200)

    def test_signup(self):
        '''
        Test if the user signup works.
        '''
        client = Client()
        response = client.post(reverse('signup'))
        self.assertTrue(response.status_code, 200)


class TestModels(TestCase):
    '''
    Test the models
    '''
    def setUp(self):
        '''
        Setting up the Product model to use it in tests functions
        '''
        self.product_test_model = Product.objects.create(
            name='Nutella model',
            description='testdescription',
            category='pâte à tartiner',
            fat=1,
            salt=1,
            image='nutella.jpg',
            sugar=1,
            nutriscore=4,
            barcode=123456789)

    def test_product(self):
        '''
        Check if the product model return the good name with the str method
        '''
        self.assertEqual(self.product_test_model.__str__(), 'Nutella model')


class TestSeleniumBrowser(LiveServerTestCase):
    '''
    This class is made to test the interaction with the browser.
    We use Selenium dependancy to test.
    To test this class you must install the following dependancies:
        (Selenium) pip install -U selenium
        (Geckodriver) brew install geckodriver (for UNIX BASE ONLY)
    '''

    def setUp(self):
        '''
        Setting up the browser and some informations to test.
        '''
        length = 8
        letters = string.ascii_lowercase
        self.test_passed = False
        self.driver = webdriver.Firefox()
        self.username = ''.join(random.choice(letters) for i in range(length))
        self.password = ''.join(random.choice(letters) for i in range(length))

    def tearDown(self):
        '''
        Function to close the navigator
        '''
        self.driver.close()

    def test_if_h1_exists(self):
        '''
        It tests if the h1 exists. It verifies the text and the classes.
        '''
        print("-------------Test if h1 title exists------------------")

        self.driver.get(test_url)
        check_h1 = self.driver.find_element_by_css_selector('h1')

        # Check if h1 exists
        self.assertTrue(check_h1)

        # Cehck if h1 has two classes name text-white and font-weight-bold
        self.assertEqual(check_h1.get_attribute('class'),
                         'text-white font-weight-bold')

        # Check if the slogan does not change
        self.assertEqual(check_h1.text, 'Du gras oui, mais de qualité !')

    def test_user_signup(self):
        '''
        Simulate a user signup. We provide the informations necessary to log
        the user.
        '''
        print("-------------Simulate a signup------------------")

        self.driver.get(test_url)

        check_form = self.driver.find_element_by_id('signup-form')
        self.assertTrue(check_form)

        form_signup = self.driver.find_element_by_id('signup-form')
        click_on_signup_encard = self.driver.find_element_by_id('signup-id')
        click_on_signup_encard.click()

        time.sleep(3)

        fill_firstname = self.driver.find_element_by_id('id_username')
        fill_firstname.click()
        fill_firstname.send_keys(self.username)

        time.sleep(2)

        fill_pwd1 = self.driver.find_element_by_id('id_password1')
        fill_pwd1.click()
        fill_pwd1.send_keys(self.password)

        time.sleep(2)

        fill_pwd2 = self.driver.find_element_by_id('id_password2')
        fill_pwd2.click()
        fill_pwd2.send_keys(self.password)

        time.sleep(2)

        form_signup.submit()

        time.sleep(2)

        self.assertEqual(self.driver.current_url,
                         test_url + "search_food/signup/")
        redirect_to_index = self.driver.find_element_by_id('redirect-to-index')
        redirect_to_index.click()

        time.sleep(3)

        check_if_user_is_logged = self.driver.find_element_by_id('welcome-to')
        self.assertEqual(check_if_user_is_logged.get_attribute(
            'title'), 'Bienvenue %s' %(self.username))

        click_on_disconnect = self.driver.find_element_by_xpath(
            '//a[@id="disconnect_user"]')
        self.driver.execute_script(
            "arguments[0].click();", click_on_disconnect)

        time.sleep(3)

        self.assertEqual(self.driver.find_element_by_id(
            'connect-user').get_attribute('title'), 'Se connecter')

    # def test_login_user(self):
    #     '''
    #     Simulate a user logging in. In this case it's a success.
    #     '''
    #     print("-------------Simulate a login------------------")

    #     self.driver.get(test_url)

    #     self.driver.find_element_by_name('username').send_keys('testuser61700')
    #     time.sleep(3)

    #     self.driver.find_element_by_name(
    #         'password').send_keys('dedansletest61')
    #     time.sleep(3)

    #     target_form = self.driver.find_element_by_css_selector(
    #         'form.signin-form')
    #     submit_button = self.driver.find_element_by_id('signin-id')

    #     self.assertTrue(submit_button)

    #     target_form.submit()
    #     time.sleep(3)
    #     click_on_carrot = self.driver.find_element_by_id('menu-favorite')
    #     self.driver.execute_script("arguments[0].click();", click_on_carrot)

    #     time.sleep(3)

    #     self.assertEqual(self.driver.current_url,
    #                      test_url + "/search_food/favorite/")

    def test_simulate_research(self):
        '''
        Simulate an entire research in the web browser.
        '''
        print("-------------Simulate a research------------------")
        self.driver.get(test_url)

        self.driver.find_element_by_name('username').send_keys('testuser61700')
        time.sleep(3)

        self.driver.find_element_by_name(
            'password').send_keys('dedansletest61')
        time.sleep(3)

        target_form = self.driver.find_element_by_css_selector(
            'form.signin-form')
        submit_button = self.driver.find_element_by_id('signin-id')

        self.assertTrue(submit_button)

        target_form.submit()

        time.sleep(2)

        self.driver.find_element_by_name('search_term').send_keys('nutella')

        time.sleep(2)

        validate_form = self.driver.find_element_by_xpath(
            '//form[contains(@class, "form-inline my-2 my-lg-0")]')
        validate_form.submit()

        time.sleep(2)
        check_h2 = self.driver.find_element_by_css_selector('h2')
        self.assertTrue(check_h2)
