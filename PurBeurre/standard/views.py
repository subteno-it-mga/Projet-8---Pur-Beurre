from django.shortcuts import render
from django.http import HttpResponse

from django.views import View
from django.contrib.auth.forms import UserCreationForm
 
class BasicViews(View):

    @staticmethod
    def index(request):
        form = UserCreationForm
        return render(request, 'standard/index.html', {'form': form})


    @staticmethod
    def favorite(request):
        return render(request,'standard/favorite.html')