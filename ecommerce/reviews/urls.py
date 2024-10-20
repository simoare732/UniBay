from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('create_review/<int:pk>/', create_review_view.as_view(), name='create_review'),
    path('update_review/<int:pk>/', update_review_view.as_view(), name='update_review'),
    path('delete_review/<int:pk>/', delete_review_view.as_view(), name='delete_review'),
]