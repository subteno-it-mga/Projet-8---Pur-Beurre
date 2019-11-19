from django.conf.urls import url
from django.urls import path
from users import views as userview

urlpatterns = [
    path('user_account/', userview.UserAccount.as_view(), name="user_account"),
    path('signup/', userview.UserAccount.signup, name="signup"),
    path('logout_user/', userview.UserAccount.logout_user, name="logout_user"),
    path('login_user/', userview.UserAccount.login_user, name="login_user"),
]