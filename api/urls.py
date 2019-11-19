from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('search/',views.CallAPI.search_and_stock, name="search_and_stock"),
    path('search_substitute/', views.CallAPI.search_substitute, name="search_substitute"),
]