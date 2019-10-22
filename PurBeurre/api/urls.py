from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('search/',views.CallAPI.search, name="search"),
]