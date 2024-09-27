from django.urls import path
from .views import create_product_view

app_name = 'listings'

urlpatterns = [
    path('create_product/', create_product_view.as_view(), name='create_product'),
]