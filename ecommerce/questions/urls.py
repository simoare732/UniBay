from django.urls import path
from .views import *

app_name = 'questions'

urlpatterns = [
    path('create_question/<int:pk>', create_question_view.as_view(), name='create_question'),
    path('questions/<int:question_id>/add_answer/', add_answer, name='add_answer'),
    path('list_questions/<int:pk>/', question_list_view.as_view(), name='list_questions'),
    path('approve_answer/<int:answer_pk>/', approve_answer, name='approve_answer'),

]