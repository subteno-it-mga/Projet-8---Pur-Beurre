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
from database.views import DatabaseManager

from unidecode import unidecode

from database.models import Product, Category, SubstituteProduct, SubstituteCategory

class CallAPI(View):
    '''
    This class is calling the api Open Food Fact.
    '''

    @staticmethod
    def change_nutriscore(nutriscore):
        '''
        change he nutriscore in the database entry to sort it in the template
        '''
        if nutriscore == "a":
            nutriscore = 1
        elif nutriscore == "b":
            nutriscore = 2
        elif nutriscore == "c":
            nutriscore = 3
        elif nutriscore == "d":
            nutriscore = 4
        elif nutriscore == "e":
            nutriscore = 5
        else:
            message_nutriscore = "Pas de Nutriscore ?"
            return message_nutriscore
        
        return nutriscore

    @staticmethod
    def search_and_stock(request):
        '''
        Get the keyword from the input form the laucnh the OPen Food Facts API call.
        '''
        term = request.POST.get('search_term')

        list_term = term.split(" ")
        final_term_list = []

        for item in list_term:
            
            if list_term[len(list_term)-1] == item:
                final_term_list.append(item)
            else:
                new_item ="".join(item+'%20')
                final_term_list.append(new_item)

        final_term_string = ''.join(final_term_list)

        url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=%s&action=process&json=1&page_size=10"%(final_term_string)
        result = urlopen(url)
        json_result = json.load(result)

        product = json_result["products"]

        DatabaseManager.create_entries(product)
        informations_displayed = DatabaseManager.display_informations(request)
        print("------------All informations will be displayed------------")
        return render(request, 'standard/product.html',{'products':informations_displayed})

    @staticmethod
    def search_subsitute(request):
        '''
        This search subsitutes from the category of the product.
        '''
        product = request.POST.get('product_barcode')
        product_end = request.POST.get('product_barcode')
        product_category = DatabaseManager.search_categories(product)
        print("------------Add Products with the same category------------")

        category_clean = unidecode(product_category)
        # url = "https://fr.openfoodfacts.org/category/%s.json" %(category_clean)
        # url = "https://world.openfoodfacts.org/cgi/search.pl?action=process&tagtype_1=categories&tag_contains_1=contains&tag_1=%s&sort_by=unique_scans_n&page_size=100&action=display&json=1" %(category_clean)
        url ="https://world.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=%s&page_size=100&axis_x=energy&axis_y=products_n&action=display&json=1" %(category_clean)
        result = urlopen(url)
        json_result = json.load(result)
        categ_product = json_result['products']

        for product in categ_product:
            try:
                description = product["generic_name"]
                name = product["product_name"]
                salt = product["nutriments"]["salt"]
                sugar = product["nutriments"]["sugars"]
                fat =  product["nutriments"]["fat"]
                nutriscore = product["nutrition_grades"]
                barcode = product["code"]
                image = product["image_front_url"]

            except KeyError:
                description = "Pas de description"
                name = "Pas de nom"
                salt = 0.0
                fat = 0.0
                sugar = 0.0
                nutriscore = "Pas de nutriscore"
                barcode = 100000
                image = "No image"

            if nutriscore == "Pas de nutriscore" or name == "Pas de nom" or name=="":
                pass
            else:
                nutriscore_db = CallAPI.change_nutriscore(nutriscore)

                data_dictionnary = {
                    'product':name,
                    'salt': salt,
                    'sugar': sugar,
                    'fat': fat,
                    'description': description,
                    'image': image,
                    'nutriscore': nutriscore_db,
                    'barcode':barcode,

                }
                DatabaseManager.substitute_products(data_dictionnary)

        substitute = DatabaseManager.display_subsitute(request)
        original_product = Product.objects.get(barcode=product_end)

        return render(request, 'standard/substitute.html', {'substitute':substitute, 'original':original_product})
