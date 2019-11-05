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
from django.urls import reverse

from django.views import View

class UserAccount(View):
    '''
    Thsi class manage the user : signin, sinup, logout, delete, add to favorite...
    '''
    def post(self, request):
        '''
        Method post to retrieve all informations from the signup form.
        '''
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            messages.add_message(request, messages.INFO, form.cleaned_data['username'])

            return HttpResponseRedirect('standard/signup.html')

        else:
            form = UserCreationForm()
            return render(request, 'standard/index.html', {'form': form})

    @staticmethod
    def login_user(request):
        '''
        Check login and password to login.
        '''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request,user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, 'standard/index.html', {'login_message':'The user doesn\'t exist','anchor':'account'})
        return render(request, 'standard/index.html')
    
    @staticmethod
    def logout_user(request):
        '''
        Logout the user if he's connnected.
        '''
        logout(request)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

    @staticmethod
    def signup(request):
        '''
        Return a page when the user created an account.
        '''
        return render(request, 'standard/signup.html')
