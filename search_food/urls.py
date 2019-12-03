from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('search/',views.search_and_stock, name="search_and_stock"),
    path('search_substitute/', views.search_substitute, name="search_substitute"),
    path('delete_entries/', views.delete_entries, name="delete_entries"),
    path('add_favorite/', views.add_favorite, name="add_favorite"),
    path('', views.index, name="index"),
    path('favorite/', views.display_favorite, name="display_favorite"),
    path('user_account/', views.user_account, name="user_account"),
    path('signup/', views.signup, name="signup"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('login_user/', views.login_user, name="login_user"),
]