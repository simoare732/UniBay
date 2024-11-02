from django.urls import path
from .views import *

app_name = 'report'

urlpatterns = [
    path('create_report/<int:pk>/', report_create_view.as_view(), name='create_report'),
    path('list_reports/', report_list_view.as_view(), name='list_reports'),
    path('delete_report/<int:pk>/', report_delete_view.as_view(), name='delete_report'),
]