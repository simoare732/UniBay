from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('create_review/<int:pk>/', create_review_view.as_view(), name='create_review'),
    path('update_review/<int:pk>/', update_review_view.as_view(), name='update_review'),
    path('delete_review/<int:pk>/', delete_review_view.as_view(), name='delete_review'),
    path('create_seller_review/<int:pk>/', create_seller_review_view.as_view(), name='create_seller_review'),
    path('update_seller_review/<int:pk>/', update_seller_review_view.as_view(), name='update_seller_review'),
    path('delete_seller_review/<int:pk>/', delete_seller_review_view.as_view(), name='delete_seller_review'),
    path('list_seller_review/<int:pk>/', list_seller_review_view.as_view(), name='list_seller_review'),
    path('list_user_review/', list_user_review_view.as_view(), name='list_user_review'),
    path('list_user_seller_review/', list_user_seller_review_view.as_view(), name='list_user_seller_review'),
]