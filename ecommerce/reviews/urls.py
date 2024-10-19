from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('create_review/<int:pk>', create_review_view.as_view(), name='create_review'),
]