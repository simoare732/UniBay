from secrets import token_urlsafe

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView

from watchlist.models import Favourite
from .models import *
from .forms import product_create_form
from users.mixins import seller_general_mixin, product_owner_mixin

class create_product_view(seller_general_mixin, CreateView):
    model = Product
    template_name = 'listings/create_product.html'
    form_class = product_create_form

    def get_success_url(self):
        return reverse('users:profile_seller', kwargs={'pk': self.object.seller.pk})

    def form_valid(self, form):
        # Save the product and set the seller
        form.instance.seller = self.request.user.seller
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seller'] = self.request.user.seller
        return context


class list_products_view(seller_general_mixin, ListView):
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


class delete_product_view(product_owner_mixin, DeleteView):
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

        if self.request.user.is_authenticated and self.request.user.is_registered_user:
            # This is to take the review of the user if it exists
            user_review = self.object.reviews.filter(reg_user=self.request.user.registered_user).first()
            if user_review:
                context['user_review'] = user_review.pk
            else:
                context['user_review'] = None

            # This is used to check if the user has already reviewed the seller
            seller_review = self.object.seller.seller_reviews.filter(reg_user=self.request.user.registered_user).first()
            if seller_review:
                context['seller_review'] = seller_review.pk
            else:
                context['seller_review'] = None

            # This is used to check if the user has already reported the seller
            report = self.request.user.registered_user.reports.filter(seller=self.object.seller).first()
            if report:
                context['report'] = report.pk
            else:
                context['report'] = None

        else:
            context['user_review'] = None
            context['seller_review'] = None

        if self.request.user.is_authenticated:
            is_favorite = Favourite.objects.filter(user=self.request.user, product=self.object).exists()
            context['is_favorite'] = is_favorite
        else:
            context['is_favorite'] = False

        # Generate a token for buy the product
        if 'checkout_token' not in self.request.session:
            self.request.session['checkout_token'] = token_urlsafe(16)
        context['checkout_token'] = self.request.session['checkout_token']


        # Obtain questions and if the user has answered to them
        questions = self.object.questions.all()

        answered_map = {}
        for q in questions:
            # The map is used to check if the user has answered to the question. If the user is not authenticated,
            # we suppose that he has not answered
            if self.request.user.is_authenticated:
                answered_map[q.pk] = q.answer.filter(user=self.request.user).exists()
            else:
                answered_map[q.pk] = False

        context['answered_map'] = answered_map

        return context

class update_product_view(product_owner_mixin, UpdateView):
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