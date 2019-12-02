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
from database.main import DatabaseManagerClass

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.shortcuts import redirect

class DatabaseManager(View):
    '''
    This class contains all methods wich work with database
    '''
    @staticmethod
    def delete_entries(request):
        '''
        Erase all database entries. ONLY FOR THE ADMIN.
        '''
        delete = DatabaseManagerClass()
        delete.delete_all_entries()

        print("--------------All entries cleaned-------------")

        return HttpResponseRedirect('/')

    @staticmethod
    @csrf_exempt
    def add_favorite(request):
        '''
        Add a substitute product in the database depend of the user.
        '''
        barcode = request.POST.get('barcode')
        user = request.user
        add_favorite = DatabaseManagerClass()
        add_favorite.add_favorite_database(int(barcode), user)

        message = "bien ajouté aux favoris"

        data = {
            'message': message,
        }
        return JsonResponse(data)