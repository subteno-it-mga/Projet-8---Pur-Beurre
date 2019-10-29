from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('delete_entries/',views.DatabaseManager.delete_entries, name="delete_entries"),
]