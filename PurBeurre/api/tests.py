from django.test import TestCase
from django.urls import reverse
import httpretty
import requests
import json
from urllib.request import urlopen

class TestAPICall(TestCase):
    '''
    This is the tests for the two API CALLS and functions in this app
    '''
    def test_change_nutriscore(self):
        '''
        Test this functionnality to substitute the letter by a number to make the sort simplier
        '''
        pass

    @httpretty.activate
    def test_search_and_stock(self):
        '''
        Test this functionnality wich is use to call API, get the JSON then stock in database.
        In this function, we'll only test the API CALL.
        We'll use Httpretty to mock the http call to OpenFoodFact API.
        '''
        # Start httpretty process.
        httpretty.enable()

        url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=nutella&action=process&json=1&page_size=1"

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

    def test_search_subsitute(self):
        '''
        Tes this functionnality wich is use to call API a second timee to retrieve products with the same category
        of the original product and stock it on the database. In this function, we'll only test the API CALL
        '''
        pass

    
