from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView
from users.mixins import admin_required_mixin

from .models import Report, Strike
from users.models import Seller
from listings.models import Product, Category
from .forms import report_create_form, strike_create_form
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



class report_list_view(admin_required_mixin, ListView):
    model = Report
    template_name = 'report/report_list.html'
    ordering = ['-date']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        #context['reports'] = Report.objects.all()
        return context


class report_delete_view(admin_required_mixin, DeleteView):
    model = Report
    template_name = 'report/report_delete.html'

    def get_success_url(self):
        return reverse('report:list_reports')


class strike_create_view(admin_required_mixin, CreateView):
    model = Strike
    form_class = strike_create_form
    template_name = 'report/strike_create.html'

    def form_valid(self, form):
        # Get the seller id from the URL
        seller_pk = self.kwargs['seller_pk']
        seller = get_object_or_404(Seller, id=seller_pk)

        # Assign the seller to the strike
        form.instance.seller = seller
        response = super().form_valid(form)

        # Check if the seller has received three strikes, if yes
        if seller.strikes.count() >= 3:
            # Email the seller
            send_mail(
                'Account sospeso',
                'Il tuo account è stato sospeso a causa di tre strike ricevuti.',
                'simoaresta3@gmail.com',
                [seller.user.email],
                fail_silently=False,
            )

            # Delete the seller
            seller.user.delete()
        else:
            # Email the seller
            send_mail(
                'Strike ricevuto',
                f'Attenzione. Hai ricevuto uno strike.\nDescrizione: {form.instance.description}',
                'simoaresta3@gmail.com',
                [seller.user.email],
                fail_silently=False,
            )

        return response

    def get_success_url(self):
        return reverse('report:list_reports')

