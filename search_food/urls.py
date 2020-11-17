'''
search_food/urls.py
This file  contains the url collection.
'''
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('search/', views.search_and_stock, name="search_and_stock"),
    path(
        'search_substitute/',
        views.search_substitute, name="search_substitute"),
    path('delete_entries/', views.delete_entries, name="delete_entries"),
    path('add_favorite/', views.add_favorite, name="add_favorite"),
    path('', views.index, name="index"),
    path('favorite/', views.display_favorite, name="display_favorite"),
    path('user_account/', views.user_account, name="user_account"),
    path('signup/', views.signup, name="signup"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('login_user/', views.login_user, name="login_user"),
    path('mention/', views.mention, name="mention"),
    path(
        'cron_database_fill',
        views.cron_database_fill,
        name='cron_database_fill'),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password/password_reset_done.html'),
        name='password_reset_done'
        ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password/password_reset_complete.html'),
        name='password_reset_complete'
        ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password/password_reset_confirm.html"),
        name='password_reset_confirm'
        ),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('i18n/', include('django.conf.urls.i18n')),
    path('languages/', views.manage_languages, name="manage_languages"),
]
