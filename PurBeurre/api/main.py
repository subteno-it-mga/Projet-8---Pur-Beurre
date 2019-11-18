from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from urllib.request import urlopen
import json
from django.http import JsonResponse
from django.contrib.auth import logout
from django.conf import settings

from django.views import View

from unidecode import unidecode

from database.models import Product, SubstituteProduct
from database.main import *

class CallAPIClass:
    '''
    This object contains all methods to access and treat all informations received by the OpenFF API.
    '''
    def __call_api_for_product(self, product):
        '''
        Private method to call the OpenFF API, retrieve products and return the json dictionnary.
        '''
        url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=%s&action=process&json=1&page_size=10" % (product)
        result = urlopen(url)
        json_result = json.load(result)
        product_dict = json_result["products"]

        return product_dict

    def __call_api_for_category(self, category):
        '''
        Private method to call the OpenFF API, retrieve category and return the json dictionnary.
        '''
        category_clean = unidecode(category)
        url = "https://world.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=%s\&page_size=100&axis_x=energy&axis_y=products_n&action=display&json=1" % (category_clean)
        result = urlopen(url)
        json_result = json.load(result)
        categ_product = json_result['products']

        return categ_product

    def treat_input_term(self, keyword):
        '''
        This function split and treat the keywords and call OpenFF API.
        '''
        keyword = unidecode(keyword)
        list_term = keyword.split(" ")
        final_term_list = []

        for item in list_term:

            if list_term[len(list_term) - 1] == item:
                final_term_list.append(item)
            else:
                new_item = "".join(item + '%20')
                final_term_list.append(new_item)

        final_term_string = ''.join(final_term_list)

        product = self.__call_api_for_product(self, final_term_string)

        DatabaseManagerClass.create_entries(self, product)

        informations_displayed = DatabaseManagerClass.display_informations(self)
        print("------------All informations will be displayed------------")

        return informations_displayed

    def retrieve_substitute(self, product_category, original_product):
        '''
        This function call the OpenFF API and store it in database.
        '''
        # TODO Call private method to retrieve category from a product _call_api_for_category
        categ_product = self.__call_api_for_category(self, product_category)
        # Loop and search for products into this json dictionnary
        for product in categ_product:
            try:
                description = product["generic_name"]
                name = product["product_name"]
                salt = product["nutriments"]["salt"]
                sugar = product["nutriments"]["sugars"]
                fat = product["nutriments"]["fat"]
                nutriscore = product["nutrition_grades"]
                barcode = product["code"]
                image = product["image_front_url"]
                category = product["compared_to_category"]

            except KeyError:
                description = "Pas de description"
                name = "Pas de nom"
                salt = 0.0
                fat = 0.0
                sugar = 0.0
                nutriscore = "Pas de nutriscore"
                barcode = 100000
                image = "No image"

            if nutriscore == "Pas de nutriscore" or name == "Pas de nom" or name == "":
                pass
            else:
                nutriscore_db = DatabaseManagerClass.change_nutriscore(DatabaseManagerClass, nutriscore)

                data_dictionnary = {
                    'product': name,
                    'salt': salt,
                    'sugar': sugar,
                    'fat': fat,
                    'description': description,
                    'image': image,
                    'nutriscore': nutriscore_db,
                    'barcode': barcode,
                    'category': category,
                    'original': original_product,
                }
                DatabaseManagerClass.substitute_products(DatabaseManagerClass, data_dictionnary)

    