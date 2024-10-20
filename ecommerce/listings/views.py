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
        return reverse('users:profile_seller', kwargs={'pk': self.object.seller.pk})

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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['seller'] = self.request.user.seller
        ctx['products'] = self.request.user.seller.products
        ctx['categories'] = Category.objects.all()
        return ctx


class delete_product_view(DeleteView):
    model = Product
    template_name = 'listings/delete_product.html'

    def get_success_url(self):
        return reverse('listings:list_products')

class detail_product_view(DetailView):
    model = Product
    template_name = 'listings/detail_product.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object
        context['categories'] = Category.objects.all()

        # This get the products of the same category of the current product
        related_products = Product.objects.filter(categories__in=self.object.categories.all()).exclude(id=self.object.id).distinct()[:5]
        context['related_products'] = related_products

        if self.request.user.is_authenticated:
            context['user_has_reviewed'] = self.object.reviews.filter(user=self.request.user).exists()
            user_review = self.object.reviews.filter(user=self.request.user).first()
            if user_review:
                context['user_review'] = user_review.pk
            else:
                context['user_review'] = None
        else:
            context['user_has_reviewed'] = False
            context['user_review'] = None

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