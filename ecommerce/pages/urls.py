from django.urls import path, include
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('list_products/', views.list_products, name='list_products'),
]