from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
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