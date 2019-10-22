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

class DatabaseManager(View):

    def create_entries(self, request, informations):
        pass

    def delete_entries(self, request, entries):
        pass

    def register_favorite(self, request, product):
        pass

    @staticmethod
    def display_informations(self, request):
        pass