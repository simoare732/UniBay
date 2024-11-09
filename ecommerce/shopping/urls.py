from django.urls import path
from .views import *

app_name = 'shopping'

urlpatterns = [
    path('list_cart/', list_cart.as_view(), name='list_cart'),
    path('update_item_quantity/<int:item_pk>/', update_cart_item_quantity, name='update_item_quantity'),

]