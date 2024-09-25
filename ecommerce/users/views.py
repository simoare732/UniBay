from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.contrib.auth import login
from .models import *
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
        # The reverse is useful to generate the URL of login page
        return redirect(reverse('users:login'))


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
        return redirect(reverse('users:login'))


# to show information of a user/seller
class detail_profile_user(DetailView):
    model = Registered_User
    template_name = 'users/profile_user.html'

class detail_profile_seller(DetailView):
    model = Seller
    template_name = 'users/profile_seller.html'