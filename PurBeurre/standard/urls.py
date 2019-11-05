from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('',views.BasicViews.index, name="index"),
    path('favorite/', views.BasicViews.display_favorite, name="display_favorite"),

]