from django.urls import path
from .views import *

app_name = 'watchlist'

urlpatterns = [
    path('toggle_favorite/<int:product_id>/', toggle_favorite, name='toggle_favorite'),
    path('list_favourites/', list_favourites.as_view(), name='list_favourites'),
    path('remove_favorite/<int:favorite_id>/', remove_favorite, name='remove_favorite'),
]