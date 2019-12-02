from django.conf.urls import url
from django.urls import path

from . import views
from .views import DatabaseManager

urlpatterns = [
    path('delete_entries/', views.DatabaseManager.delete_entries, name="delete_entries"),
    path('add_favorite/', views.DatabaseManager.add_favorite, name="add_favorite"),
]