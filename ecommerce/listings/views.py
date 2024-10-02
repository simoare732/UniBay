from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from .models import *
from .forms import product_create_form


class create_product_view(CreateView):
    model = Product
    template_name = 'listings/create_product.html'
    #fields = '__all__'
    form_class = product_create_form

    def get_success_url(self):
        return reverse_lazy('users:profile_seller', kwargs={'pk': self.object.seller.pk})

    def form_valid(self, form):
        # Pass the current user to the form
        #form.save(user=self.request.user)
        form.instance.seller = self.request.user.seller
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seller'] = self.request.user.seller
        return context


class list_products_view(ListView):
    model = Product
    template_name = 'listings/list_products.html'
    ordering = ['-date']
    paginate_by = 10


class delete_product_view(DeleteView):
    model = Product
    template_name = 'listings/delete_product.html'

    def get_success_url(self):
        return reverse('listings:list_products')

class deatil_product_view(DetailView):
    model = Product
    template_name = 'listings/detail_product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object
        return context

class update_product_view(UpdateView):
    #BUG: even if there are images for a product, the form for the images shows 'No file chosen'. If you press 'Modifica'
    # the images there are.
    model = Product
    template_name = 'listings/update_product.html'
    form_class = product_create_form


    def get_success_url(self):
        return reverse('listings:list_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seller'] = self.request.user.seller
        return context