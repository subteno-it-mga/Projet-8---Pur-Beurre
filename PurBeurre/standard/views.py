from django.shortcuts import render
from django.http import HttpResponse

from django.views import View
from django.contrib.auth.forms import UserCreationForm

from database.models import Product, SubstituteProduct, Favorite
 
class BasicViews(View):
    '''
    Return all basics views.
    '''
    @staticmethod
    def index(request):
        '''
        Display the form in the main page.
        '''
        form = UserCreationForm
        return render(request, 'standard/index.html', {'form': form})


    @staticmethod
    def display_favorite(request):
        '''
        TO DO : Display the favorite products saved by users.
        '''
        actual_user = request.user
        retrieve_favorite = Favorite.objects.filter(user_associated=actual_user)
        
        return render(request,'standard/favorite.html', {'product':retrieve_favorite})
