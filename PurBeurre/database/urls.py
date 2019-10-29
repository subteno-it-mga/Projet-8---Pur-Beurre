from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('delete_entries/',views.DatabaseManager.delete_entries, name="delete_entries"),
    path('search_categories', views.DatabaseManager.search_categories, name="search_categories"),
]