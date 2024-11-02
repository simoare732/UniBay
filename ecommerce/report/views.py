from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from .models import Report
from users.models import Seller
from listings.models import Product
from .forms import report_create_form


class report_create_view(CreateView):
    model = Report
    form_class = report_create_form
    template_name = 'report/report_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(pk=self.kwargs.get('pk'))
        context['product'] = product
        context['seller'] = Seller.objects.get(pk=product.seller.pk)
        return context

    def form_valid(self, form):
        product = Product.objects.get(pk=self.kwargs.get('pk'))
        form.instance.reporter = self.request.user.registered_user
        form.instance.seller = Seller.objects.get(pk=product.seller.pk)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('listings:detail_product', kwargs={'pk': self.kwargs.get('pk')})