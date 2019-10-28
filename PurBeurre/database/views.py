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
from database.models import Product, Category

class DatabaseManager(View):

    @staticmethod
    def create_categories(list_of_categories):
        for category in list_of_categories:
            result = [x.strip() for x in category["categories"].split(',')]
            for categories in result:
                if not Category.objects.filter(name=categories):
                    categ = Category(name=categories)
                    categ.save()

        

    @staticmethod
    def create_entries(informations, categories):
        # name = informations[0]["product_name"]
        # # product_img = json_result["products"][0]["image_front_url"]
        # salt = informations[0]["nutriments"]["salt"]
        # sugar = informations[0]["nutriments"]["sugars"]
        # fat = informations[0]["nutriments"]["fat"]
        # nutriscore = informations[0]["nutrition_grades"]
        # barcode = informations[0]["code"]        
        # DatabaseManager.create_categories(categories)

        for product in informations:
            description = "Message générique"
            name = product["product_name"]
            salt = product["nutriments"]["salt"]
            sugar = product["nutriments"]["sugars"]
            fat = product["nutriments"]["fat"]
            nutriscore = product["nutrition_grades"]
            barcode = product["code"]
            categories = product["categories"]
            c = Product(name=name, salt= salt, sugar=sugar, fat=fat, nutriscore=nutriscore, barcode=barcode, description=description)
            c.save()
            d = Category(name=categories, product=c)
            d.save()

            # for category in categories:
            #     result = [x.strip() for x in category["categories"].split(',')]
            #     import pdb; pdb.set_trace()
            #     for category_list in result:
                    
            # import pdb; pdb.set_trace()
            # c.categories.name = "Petit-déjeuners"
            # c.save()
            # d = Category.objects.filter(name="Petit-déjeuners")

            # e = Product.objects.filter(name="Nutella")
            # import pdb; pdb.set_trace()
            # e.categories.add(d)
            # e.save()
            # for category in categories:
            #     result = [x.strip() for x in categories.split(',')]
            #     import pdb; pdb.set_trace()
            #     c.categories.add(result)
            #     c.save()
            # c.save()
            # for category in categories:
            #     result = [x.strip() for x in category["categories"].split(',')]
            #     for product_category in result:
            #         categ = Category.objects.get(name=product_category)
            #         if not categ:
            #             c.categories.add(categ)
            #         else:
            #             c.categories.add(categ)


    def delete_entries(self, request, entries):
        pass

    def register_favorite(self, request, product):
        pass

    @staticmethod
    def display_informations(self, request):
        pass