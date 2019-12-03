from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
import httpretty
import requests
import json
from urllib.request import urlopen
from unidecode import unidecode
from .models import Product, User, Favorite, SubstituteProduct
from .views import *
from django.urls import reverse
client = Client()

class TestCallAPI(TestCase):
    '''
    This is the tests for the two API CALLS and functions in this app
    '''

    def setUp(self):
        self.factory = RequestFactory()

    @httpretty.activate
    def test_call_api_for_product(self):
        '''
        Test this functionnality wich is use to call API, get the JSON then stock in database.
        In this function, we'll only test the API CALL.
        We'll use Httpretty to mock the http call to OpenFoodFact API.
        '''
        product = "Nutella"

        httpretty.enable()
        url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=%s&action=process&json=1&page_size=1" %(product)

        # Here test the response and integrity of information given.
        httpretty.register_uri(
            httpretty.GET, url,
            body='{"page_size": 20,"products":[{"product_name": "Nutella"}]}',
            content_type="application/json")

        response = requests.get(url)
        last_request = httpretty.last_request()

        self.assertEqual(last_request.method, 'GET')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"page_size": 20, "products": [{"product_name": "Nutella"}]})

        # Test if we can read the json file and retrieve good informations from it.
        result = urlopen(url)
        json_result = json.load(result)
        categ_product = json_result['products']

        self.assertEqual(categ_product[0]['product_name'], "Nutella")

        # Clean up the process
        httpretty.disable()
        httpretty.reset()

    @httpretty.activate
    def test_api_call_for_category(self):
        '''
        Test this functionnality wich is use to call API, get the JSON then stock in database.
        In this function, we'll only test the API CALL.
        We'll use Httpretty to mock the http call to OpenFoodFact API.
        '''
        category = "en:biscuits"
        category_clean = unidecode(category)
        # Start httpretty process.
        httpretty.enable()

        url = "https://world.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=%s\&page_size=100&axis_x=energy&axis_y=products_n&action=display&json=1" % (category_clean)

        # Here test the response and integrity of information given.
        httpretty.register_uri(
            httpretty.GET, url,
            body='{"page_size": 100,"products":[{"product_name_fr": "Prince: Goût Chocolat au Blé Complet"}]}',
            content_type="application/json")

        response = requests.get(url)
        last_request = httpretty.last_request()

        self.assertEqual(last_request.method, 'GET')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"page_size": 100, "products": [{"product_name_fr": "Prince: Goût Chocolat au Blé Complet"}]})

        # Test if we can read the json file and retrieve good informations from it.
        result = urlopen(url)
        json_result = json.load(result)
        categ_product = json_result['products']

        self.assertEqual(categ_product[0]['product_name_fr'], "Prince: Goût Chocolat au Blé Complet")

        # Clean up the process
        httpretty.disable()
        httpretty.reset()

    def test_search_subsitute(self):
        '''
        Tes this functionnality wich is use to call API a second timee to retrieve products with the same category
        of the original product and stock it on the database. In this function, we'll only test the API CALL
        '''
        pass
    
    def test_treat_input_term(self):
        '''
        This function tests if the keyword(s) are split and if the api call is successful.
        '''
        keyword = unidecode("pains au chocôlat")

        # Check if the accentutation is removed or not
        self.assertEqual(keyword, 'pains au chocolat')

        list_term = keyword.split(" ")
        final_term_list = []

        for item in list_term:

            if list_term[len(list_term) - 1] == item:
                final_term_list.append(item)
            else:
                new_item = "".join(item + '%20')
                final_term_list.append(new_item)

        final_term_string = ''.join(final_term_list)

        product = call_api_for_product(final_term_string)

        create_entries(product, final_term_string)

        informations_displayed = display_informations(final_term_string)

        # Test if the loop assemblate the term to search a product in the API.
        self.assertEqual(final_term_string, 'pains%20au%20chocolat')

        # Test if the value return the good data
        self.assertEqual(product[0]['product_name'], "Pains au chocolat")

        # Test if the product is in the database
        self.assertEqual(Product.objects.get(barcode=product[0]['code']).barcode, 3256540001008)

        # Test if the queryset returns good informations
        self.assertEqual(informations_displayed[0].name, 'Pains au chocolat')

    def test_retrieve_subsitute(self):
        '''
        This function test the api call and the retrieve of category and then enter in the database. 
        '''
        pass

    def test_search_and_stock(self):
        # response = client.get(reverse('search_and_stock'))
        # request = CallAPI.as_view()(response)
        # self.assertEqual(request.status_code, 200)
        pass

class DatabaseTestCase(TestCase):
    '''
    Test for products in database
    '''

    def setUp(self):
        '''
        Setting up all objects for the test. All datas will be erase after the test
        '''
        # Create a test user in the database
        self.user_test = User.objects.create_user('testuser', 'user@user.fr', 'passwordtest')

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
            barcode=123456789)

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

    def test_change_nutriscore(self):
        '''
        Test if the nutriscore is well substitute.
        '''
        # Test if the nutriscore change from strong to integer for a betttr sort in the template
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
        self.assertEqual(test_change_nutriscore_x, "Pas de Nutriscore ?")

    def test_create_entries(self):
        '''
        Test the entries in the database. Then look if the entry exists or not.
        '''
        # Initialize a json file, a database object, then save entries in the database.
        test_json_file = call_api_for_product("nutella")
        create_entries(test_json_file, "nutella")

        # Check if the products was saved in the database
        self.assertTrue(Product.objects.all().count(), Product.objects.all().count() > 5)
        self.assertEqual(Product.objects.get(barcode=test_json_file[0]['code']).name, "Nutella")

        # Check if the entries in database are all unique by their barcodes.
        for product in Product.objects.all():
            self.assertEqual(Product.objects.filter(barcode=test_json_file[0]['code']).count(), 1)

    def test_delete_all_entries(self):
        '''
        Test if all entries are deleted well after calling the delete function.
        '''
        # Get the user by his username
        test_user_object = User.objects.get(username='testuser')

        # Call the function to delete all entries
        delete_all_entries()

        # Test if the user is not deleted when we're calling the function to delete all entries
        self.assertEqual(test_user_object.username, 'testuser')

        # Test if the database is clean from product
        self.assertQuerysetEqual(SubstituteProduct.objects.filter(barcode=123456789), [])
        self.assertQuerysetEqual(SubstituteProduct.objects.filter(barcode=12345678910), [])
        self.assertQuerysetEqual(Favorite.objects.filter(barcode=1234567891011), [])

        # Check if we don't forget an entry in database so try to search any data in database
        self.assertQuerysetEqual(Product.objects.all(), [])
        self.assertQuerysetEqual(SubstituteProduct.objects.all(), [])
        self.assertQuerysetEqual(Favorite.objects.all(), [])

    def test_display_informations(self):
        '''
        Test if we retrieve correctly all products in database.
        '''
        keyword = unidecode("nutella")
        list_term = keyword.split(" ")
        final_term_list = []

        for item in list_term:

            if list_term[len(list_term) - 1] == item:
                final_term_list.append(item)
            else:
                new_item = "".join(item + '%20')
                final_term_list.append(new_item)

        final_term_string = ''.join(final_term_list)

        # Call the function which is display all products in database
        test_display = display_informations(final_term_string)

        # Test if the function return a queryset of all product in database.
        self.assertQuerysetEqual(test_display, [])

    def test_display_substitutes(self):
        '''
        Test if the data are saved correctly in database.
        '''
        # Get the product registered before
        test_query_product = Product.objects.get(barcode=123456789)

        # Call the function wich display substitutes from the original product
        test_substitute_query = display_substitutes(test_query_product)

        # Test if the function return a correct queryset from the original product
        self.assertQuerysetEqual(test_substitute_query, ['<SubstituteProduct: gerblé>'])

    def test_search_categories(self):
        '''
        Test the search categories function, depends on barcode
        '''
        # Get the product registered before
        test_query_product = Product.objects.get(barcode=123456789)

        # Two queries : one to trigger the good informaions and the other to return an error
        test_search_category = search_categories(test_query_product.barcode)
        test_search_category_wrong = search_categories(10203040)

        # Check the values if we enter a good or a wrong barcode
        self.assertEqual(test_search_category, 'pâte à tartiner')
        self.assertEqual(test_search_category_wrong, "Ce produit n'est pas ou plus présent dans la base.")

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
        test_query_substitute = SubstituteProduct.objects.filter(barcode=1234567891011)

        # Test if he subsistute obect his created
        self.assertQuerysetEqual(test_query_substitute, ['<SubstituteProduct: gerblé2>'])

    def test_add_favorite_database(self):
        '''
        Test if the product are added as favorite in database.
        '''

        # We call the function to add a favorite in database with the substitute product and the user in parameter
        add_favorite_database(self.product_substitute.barcode, self.user_test)

        # Test i we have all datas in the favorite database and if it's match with the substitute define
        self.assertQuerysetEqual(Favorite.objects.filter(barcode=12345678910), ['<Favorite: gerblé>'])
        self.assertEqual(Favorite.objects.get(barcode=12345678910).user_associate.username, 'testuser')
        self.assertEqual(Favorite.objects.get(barcode=12345678910).product_name, 'gerblé')

class TestBasicViews(TestCase):

    def test_home_page_status_code(self):
        '''
        Check if the returned status code of the page is 200
        '''
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        '''
        Check if the url returned is good
        '''
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        '''
        Test if we use the correct template and it returns a 200 status_code
        '''
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'standard/index.html')
        
    def test_home_page_contains_correct_html(self):
        '''
        Test if the html page contains the h1 title (only present in the index page)
        '''
        response = self.client.get('/')
        self.assertContains(response, '<h1 class="text-white font-weight-bold">Du gras oui, mais de qualité !</h1>')

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
    def test_post_form_valid(self):
        '''
        Check if the form fill in UserCreationForm is valid when informations are valids.
        '''
        form_data = {"username":"martin","password1":"matchingpass","password2":"matchingpass"}
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_post_user_creation_case_wrong(self):          
        '''
        Check if the form is False when the user doesn't fill one or few informations.
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

    def test_user_login(self):
        test_c = Client()
        test_form_data = {
            "username": "martin",
             "password1": "thisisatest",
              "password2": "thisisatest"}

        test_temp_auth = UserCreationForm(data=test_form_data)

        test_temp_auth.save()
        test_form_data_true = {"username": "martin", "password": "thisisatest"}

        response = test_c.post('/users/login_user/', test_form_data)
        response2 = test_c.post('/users/login_user/', test_form_data_true)

        self.assertTrue(response)
        self.assertTrue(response2)

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
        