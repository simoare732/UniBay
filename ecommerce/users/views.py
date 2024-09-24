from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from .models import User
from .forms import User_Signup_Form, Seller_Signup_Form


def home_signup(request):
    return render(request, 'users/home_signup.html')


class User_Signup_View(CreateView):
    model = User
    form_class = User_Signup_Form
    template_name = 'users/user_signup.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_type'] = 'utente'
        return ctx

    def form_valid(self , form):
        user = form.save()
        login(self.request, user)
        return redirect('pages:home_page')


class Seller_Signup_View(CreateView):
    model = User
    form_class = Seller_Signup_Form
    template_name = 'users/user_signup.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user_type'] = 'venditore'
        return ctx

    def form_valid(self , form):
        user = form.save()
        login(self.request, user)
        return redirect('pages:home_page')