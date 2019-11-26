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
from api.main import CallAPIClass
from database.main import DatabaseManagerClass


class CallAPI(View):
    '''
    This class returning the views related to API CALL.
    '''
    @staticmethod
    def search_and_stock(request):
        '''
        Get the keyword from the input form the laucnh the OPen Food Facts API call.
        '''
        term = request.POST.get('search_term')

        final_information = CallAPIClass.treat_input_term(CallAPIClass, term)
        return render(request, 'standard/product.html', {'products': final_information})

    @staticmethod
    def search_substitute(request):
        '''
        This search subsitutes from the category of the product.
        '''
        product = request.POST.get('product_barcode')
        original_product = Product.objects.get(barcode=product)
        product_category = DatabaseManagerClass.search_categories(DatabaseManagerClass, product)
        CallAPIClass.retrieve_substitute(CallAPIClass, product_category, original_product)
        
        print("------------Add Products with the same category------------")

        substitute = DatabaseManagerClass.display_substitutes(DatabaseManagerClass, original_product)

        return render(request, 'standard/substitute.html', {'substitute': substitute, 'original': original_product})