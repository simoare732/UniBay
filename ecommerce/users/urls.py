from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('', views.home_signup, name='home_signup'),
    path('usersignup/', views.User_Signup_View.as_view(), name='user_signup'),
    path('sellersignup/', views.Seller_Signup_View.as_view(), name='seller_signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]