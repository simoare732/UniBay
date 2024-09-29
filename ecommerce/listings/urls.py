from django.urls import path
from .views import *

app_name = 'listings'

urlpatterns = [
    path('create_product/', create_product_view.as_view(), name='create_product'),
    path('list_products/', list_products_view.as_view(), name='list_products'),

    path('delete_product/<int:pk>/', delete_product_view.as_view(), name='delete_product'),
    path('detail_product/<int:pk>/', deatil_product_view.as_view(), name='detail_product'),

]