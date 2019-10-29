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

from django.shortcuts import redirect

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
    def create_entries(informations):

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
                categories = [x.strip() for x in product["categories"].split(',')]
                c = Product(name=name, salt= salt, sugar=sugar, fat=fat, nutriscore=nutriscore, barcode=barcode, description=description, image=image)
                c.save()
                for category in categories:
                    d = Category(name=category, product=c)
                    d.save()
    @staticmethod
    def delete_entries(request):
        Product.objects.all().delete()
        context = {
            'confirmation':'Les données ont bien été supprimées.'
        }
        return render(request,'standard/index.html', context)

    def register_favorite(self, request, product):
        pass

    @staticmethod
    def display_informations(request):
        print("-------------We are retrieving all objects-------------")
        my_product = Product.objects.all()
        return my_product
    
    @staticmethod
    def search_categories(barcode):
        try:
            the_product = Product.objects.filter(barcode=barcode)
            product_categories = the_product.categories_set.all()
            return product_categories
        except:
            message_information = "Ce produit n'est pas ou plus présent dans la base."
            return message_information


