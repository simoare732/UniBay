from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home_signup, name='home_signup'),
]