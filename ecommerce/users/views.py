from django.shortcuts import render
from django.views.generic import CreateView


def home_signup(request):
    return render(request, 'users/home_signup.html')

