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

from database.models import Product, Category, SubstituteProduct, SubstituteCategory



from django.shortcuts import redirect

class DatabaseManager(View):
    '''
    This class contains all methods wich work with database
    '''
    @staticmethod
    def change_nutriscore(nutriscore):
        '''
        Change nutriscore for database entries.
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
    def create_categories(list_of_categories):
        '''
        Read the string of the categories obtained from the api
        '''
        for category in list_of_categories:
            result = [x.strip() for x in category["categories"].split(',')]
            for categories in result:
                if not Category.objects.filter(name=categories):
                    categ = Category(name=categories)
                    categ.save()

    @staticmethod
    def create_entries(informations):
        '''
        Creat entries for the products from the json file obtained from the
        OpenFoodFact API.
        '''
        print("-------------We are creating products-------------")

        for product in informations:
            try:
                description = product["generic_name"]
                name = product["product_name"]
                salt = product["nutriments"]["salt"]
                sugar = product["nutriments"]["sugars"]
                fat = product["nutriments"]["fat"]
                nutriscore = product["nutrition_grades"]
                barcode = product["code"]
                image = product["image_front_url"]
                category_test = product["compared_to_category"]
            except KeyError:
                description = "Pas de description"
                name = "Pas de nom"
                salt = 0.0
                fat = 0.0
                sugar = 0.0
                nutriscore = "Pas de nutriscore"
                barcode = 100000
                image = "No image"
            else:
                if nutriscore == "Pas de nutriscore" or name == "Pas de nom" or name=="":
                    pass
                else:
                    nutriscore_modified = DatabaseManager.change_nutriscore(nutriscore)
                    c = Product(name=name, salt= salt, sugar=sugar, fat=fat, nutriscore=nutriscore_modified,
                        barcode=barcode, description=description, image=image, category_test=category_test)
                    c.save()
                    print(c)


    @staticmethod
    def delete_entries(request):
        '''
        Erase all database entries. ONLY FOR THE ADMIN.
        '''
        Product.objects.all().delete()
        SubstituteProduct.objects.all().delete()
        context = {
            'confirmation':'Les données ont bien été supprimées.'
        }
        return render(request,'standard/index.html', context)

    def register_favorite(self, request, product):
        pass

    @staticmethod
    def display_informations(request):
        '''
        Display all products on page to choose a product to compare.
        '''
        print("-------------We are retrieving all objects-------------")
        my_product = Product.objects.all()
        return my_product
    
    @staticmethod
    def display_subsitute(request):
        '''
        This function returns all products found to substitute.
        '''
        print("---------------Display substitutes found----------------")
        substitute = SubstituteProduct.objects.all()
        return substitute
    
    @staticmethod
    def search_categories(barcode):
        '''
        Search Categories in the database to retrive them in the api.
        '''
        try:
            product_categories = Product.objects.get(barcode=barcode)
            return product_categories.category_test
        except:
            message_information = "Ce produit n'est pas ou plus présent dans la base."
            return message_information

    @staticmethod
    def substitute_products(data_dict):
        '''
        Add all subsitute in the database.
        '''
        d = SubstituteProduct(name=data_dict['product'], salt=data_dict['salt'], sugar=data_dict['sugar'],
            fat=data_dict['fat'], nutriscore=data_dict['nutriscore'], barcode=data_dict['barcode'],
                description=data_dict['description'], image=data_dict['image'])
        d.save()
            
            
            
