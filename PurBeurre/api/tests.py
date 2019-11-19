from django.test import TestCase
from django.urls import reverse
import httpretty
import requests
import json
from urllib.request import urlopen
from unidecode import unidecode
from api.main import *
from database.main import CallAPIClass, DatabaseManagerClass
from database.models import Product

class TestCallAPICall(TestCase):
    '''
    This is the tests for the two API CALLS and functions in this app
    '''
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

        product = CallAPIClass.call_api_for_product(CallAPIClass, final_term_string)

        DatabaseManagerClass.create_entries(self, product)

        informations_displayed = DatabaseManagerClass.display_informations(self)

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



