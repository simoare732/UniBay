from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from .models import Report
from users.models import Seller
from listings.models import Product, Category
from .forms import report_create_form
from django.contrib.auth.mixins import UserPassesTestMixin


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



class report_list_view(UserPassesTestMixin, ListView):
    model = Report
    template_name = 'report/report_list.html'
    ordering = ['-date']


    def test_func(self):
        # Check if the user is staff or superuser
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        # If the user is not staff or superuser, redirect to the home page
        #messages.error(self.request, "Non hai i permessi per accedere a questa pagina.")
        return redirect('pages:home_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        #context['reports'] = Report.objects.all()
        return context


class report_delete_view(UserPassesTestMixin, DeleteView):
    model = Report
    template_name = 'report/report_delete.html'

    def test_func(self):
        # Check if the user is staff or superuser
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        # If the user is not staff or superuser, redirect to the home page
        #messages.error(self.request, "Non hai i permessi per accedere a questa pagina.")
        return redirect('pages:home_page')

    def get_success_url(self):
        return reverse('report:list_reports')