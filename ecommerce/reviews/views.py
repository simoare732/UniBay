from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from listings.models import Product, Category
from users.models import Seller
from .models import Review, Seller_Review
from .forms import *

class create_review_view(CreateView):
    model = Review
    template_name = 'reviews/create_review.html'
    form_class = review_create_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()
        context['product'] = Product.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        product_id = self.kwargs.get('pk')  # Ottieni l'ID del prodotto dalla URL
        form.instance.product = Product.objects.get(pk=product_id)  # Associa la recensione al prodotto
        form.instance.reg_user = self.request.user.registered_user  # Associa la recensione all'utente loggato
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('listings:detail_product', kwargs={'pk': self.kwargs['pk']})


class update_review_view(UpdateView):
    model = Review
    template_name = 'reviews/update_review.html'
    form_class = review_create_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.get_object()
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()
        context['product'] = review.product
        return context

    def get_success_url(self):
        review = self.get_object()
        return reverse('listings:detail_product', kwargs={'pk': review.product.pk})


class delete_review_view(DeleteView):
    model = Review
    template_name = 'reviews/delete_review.html'

    def get_success_url(self):
        review = self.get_object()
        return reverse('listings:detail_product', kwargs={'pk': review.product.pk})



class create_seller_review_view(CreateView):
    model = Seller_Review
    template_name = 'reviews/create_seller_review.html'
    form_class = seller_review_create_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()
        context['seller'] = Seller.objects.get(pk=self.kwargs['pk'])

        # Recupera il product_pk dai query parameters
        product_pk = self.request.GET.get('product_pk')
        if product_pk:
            context['product'] = product_pk
        else:
            context['product'] = None

        return context

    def form_valid(self, form):
        seller_id = self.kwargs.get('pk')  # Ottieni l'ID del venditore dalla URL
        seller = Seller.objects.get(pk=seller_id)  # Ottieni l'istanza del venditore
        form.instance.seller = seller  # Associa l'oggetto User del venditore alla recensione
        form.instance.reg_user = self.request.user.registered_user  # Associa la recensione all'utente loggato
        return super().form_valid(form)

    def get_success_url(self):
        product_pk = self.request.GET.get('product_pk')
        if product_pk:
            return reverse('listings:detail_product', kwargs={'pk': product_pk})
        else:
            return reverse('pages:home_page')


class update_seller_review_view(UpdateView):
    model = Seller_Review
    template_name = 'reviews/update_seller_review.html'
    form_class = seller_review_create_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller_review = self.get_object()
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()
        context['seller'] = seller_review.seller

        # Recupera il product_pk dai query parameters
        product_pk = self.request.GET.get('product_pk')
        if product_pk:
            context['product'] = product_pk
        else:
            context['product'] = None

        return context

    def get_success_url(self):
        product_pk = self.request.GET.get('product_pk')
        if product_pk:
            return reverse('listings:detail_product', kwargs={'pk': product_pk})
        else:
            return reverse('pages:home_page')


class delete_seller_review_view(DeleteView):
    model = Seller_Review
    template_name = 'reviews/delete_seller_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recupera il product_pk dai query parameters
        product_pk = self.request.GET.get('product_pk')
        if product_pk:
            context['product'] = product_pk
        else:
            context['product'] = None

        return context

    def get_success_url(self):
        product_pk = self.request.GET.get('product_pk')
        if product_pk:
            return reverse('listings:detail_product', kwargs={'pk': product_pk})
        else:
            return reverse('pages:home_page')


class list_seller_review_view(ListView):
    model = Seller_Review
    template_name = 'reviews/list_seller_review.html'
    ordering = ['-date']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()

        seller_pk = self.kwargs.get('pk')
        context['seller'] = Seller.objects.get(pk=seller_pk)

        context['seller_reviews'] = Seller_Review.objects.filter(seller=context['seller'])

        # Recupera il product_pk dai query parameters
        product_pk = self.request.GET.get('product_pk')
        if product_pk:
            context['product'] = product_pk
        else:
            context['product'] = None

        return context


class list_user_review_view(ListView):
    model = Review
    template_name = 'reviews/list_user_review.html'
    ordering = ['-date']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()
        context['reg_user'] = self.request.user.registered_user

        return context


class list_user_seller_review_view(ListView):
    model = Seller_Review
    template_name = 'reviews/list_user_seller_review.html'
    ordering = ['-date']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()
        context['reg_user'] = self.request.user.registered_user

        return context