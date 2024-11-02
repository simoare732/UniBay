from django.urls import path
from .views import *

app_name = 'report'

urlpatterns = [
    path('create_report/<int:pk>/', report_create_view.as_view(), name='create_report'),
]