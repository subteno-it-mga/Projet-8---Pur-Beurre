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

from database.models import Product, SubstituteProduct, Favorite
from api.main import *


class DatabaseManagerClass:
    '''
    This object create, delete and sort items in database.
    '''
    def change_nutriscore(self, nutriscore):
        '''
        Change the nutriscore in the database entry to sort it simplier in the template
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

    def create_entries(self, informations):
        '''
        Create the entires in database for the searched product.
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

            else:
                if nutriscore == "Pas de nutriscore" or name == "Pas de nom" or name == "":
                    pass
                else:
                    if Product.objects.filter(barcode=barcode) == '':
                        pass
                    else:
                        nutriscore_modified = DatabaseManagerClass.change_nutriscore(self, nutriscore)
                        c = Product(
                            name=name,
                            salt=salt,
                            sugar=sugar,
                            fat=fat,
                            nutriscore=nutriscore_modified,
                            barcode=barcode,
                            description=description,
                            image=image,
                            category=category)
                        c.save()
                        print(c)
        print("---------------All products are correctly in base------------")

    def delete_all_entries(self):
        '''
        Delete all the entries in the database. ONLY FOR ADMIN.
        '''
        Product.objects.all().delete()
        SubstituteProduct.objects.all().delete()
        Favorite.objects.all().delete()

    def display_informations(self):
        '''
        Search all original products in Database.
        '''
        return Product.objects.all()

    def display_substitutes(self, original_product):
        '''
        Display all product substitute from the original product.
        '''
        return SubstituteProduct.objects.filter(original=original_product)

    def search_categories(self, barcode):
        '''
        Search Categories in the database to retrieve them in the api.
        '''
        try:
            product_categories = Product.objects.get(barcode=barcode)
            return product_categories.category
        except Product.DoesNotExist:
            message_information = "Ce produit n'est pas ou plus présent dans la base."
            return message_information

    def substitute_products(self, data_dict):
        '''
        Add all substitute in the database.
        '''
        d = SubstituteProduct(
            name=data_dict['product'],
            salt=data_dict['salt'], sugar=data_dict['sugar'],
            fat=data_dict['fat'],
            nutriscore=data_dict['nutriscore'],
            barcode=data_dict['barcode'],
            description=data_dict['description'],
            image=data_dict['image'],
            category=data_dict['category'],
            original=data_dict['original'])
        d.save()

    def add_favorite_database(self, favorite, user):
        '''
        Add a substitute product in the database depends of the user.
        '''
        product_associate = SubstituteProduct.objects.get(barcode=favorite)

        actual_user = user

        save_favorite = Favorite(
                        product_associate=product_associate,
                        user_associate=actual_user,
                        product_name=product_associate.name,
                        barcode=product_associate.barcode)
        save_favorite.save()
        print("-----------The favorite was added into database---------------")