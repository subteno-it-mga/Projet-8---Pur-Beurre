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

class CallAPI(View):

    @staticmethod
    def search(request):
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

        url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=%s&action=process&json=1"%(final_term_string)
        result = urlopen(url)
        json_result = json.load(result)

        # product_title = json_result["products"][0]["product_name"]
        # product_img = json_result["products"][0]["image_front_url"]
        # product_salt = json_result["products"][0]["nutriments"]["salt"]
        # product_fat = json_result["products"][0]["nutriments"]["fat"]
        # product_nutriscore = json_result["products"][0]["nutrition_grades"]

        product = json_result["products"]

        context = {

            # 'product_title': product_title,
            # 'product_img' : product_img,
            # 'product_salt': product_salt,
            # 'product_fat': product_fat,
            # 'product_nutriscore': product_nutriscore,
            'products':product, 
        }

        return render(request, 'standard/product.html',context)