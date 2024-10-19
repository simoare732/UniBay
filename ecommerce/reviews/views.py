from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from listings.models import Category, Product
from .models import Review
from .forms import review_create_form

class create_review_view(CreateView):
    model = Review
    template_name = 'reviews/create_review.html'
    form_class = review_create_form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        product_id = self.kwargs.get('pk')  # Ottieni l'ID del prodotto dalla URL
        form.instance.product = Product.objects.get(pk=product_id)  # Associa la recensione al prodotto
        form.instance.user = self.request.user  # Associa la recensione all'utente loggato
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('listings:detail_product', kwargs={'pk': self.kwargs['pk']})
