from django.shortcuts import render
from django.http import HttpResponse

from django.views import View
 
class BasicViews(View):

    @staticmethod
    def index(request):

        return render(request, 'standard/index.html')

    @staticmethod
    def favorite(request):
        return render(request,'favorite.html')