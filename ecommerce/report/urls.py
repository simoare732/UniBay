from django.urls import path
from .views import *

app_name = 'report'

urlpatterns = [
    path('create_report/<int:pk>/', report_create_view.as_view(), name='create_report'),
    path('list_reports/', report_list_view.as_view(), name='list_reports'),
    #path('delete_report/<int:pk>/', report_delete_view.as_view(), name='delete_report'),
    path('create_strike/<int:seller_pk>/', strike_create_view.as_view(), name='create_strike'),
    path('mark_seen/<int:report_pk>/', mark_report_seen, name='mark_report_seen'),
]