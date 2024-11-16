from django.urls import path
from .views import *

app_name = 'shopping'

urlpatterns = [
    path('list_cart/', list_cart.as_view(), name='list_cart'),
    path('update_item_quantity/<int:item_pk>/', update_cart_item_quantity, name='update_item_quantity'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('checkout/', checkout_view.as_view(), name='checkout'),
    path('order_success/', order_success, name='order_success'),
    path('order_list/', order_list_view.as_view(), name='order_list'),
    path('order_seller_list', order_seller_list_view.as_view(), name='order_seller_list'),
    path('update_order/<int:item_id>/', update_order, name='order_update'),

]