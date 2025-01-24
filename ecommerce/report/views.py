from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, DeleteView
from users.mixins import admin_required_mixin, reguser_general_mixin

from .models import Report, Strike
from users.models import Seller
from listings.models import Product, Category
from .forms import report_create_form, strike_create_form

class report_create_view(reguser_general_mixin, CreateView):
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

    def get_queryset(self):
        return Report.objects.filter(seen=False).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


@require_POST
def mark_report_seen(request, report_pk):
    report = get_object_or_404(Report, pk = report_pk)

    report.set_seen()

    # After marking the report as seen, redirect to the list of reports
    return redirect('report:list_reports')

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
                'Account eliminato',
                'Il tuo account è stato eliminato a causa di tre strike ricevuti.',
                'simoaresta3@gmail.com',
                [seller.user.email],
                fail_silently=False,
            )

            # Delete the seller
            seller.user.delete()
        else:
            msg = f'Hai ricevuto uno strike. Descrizione: {form.instance.description}'
            # Email the seller
            send_mail(
                'Strike ricevuto',
                msg,
                'admin@admin.com',
                [seller.user.email],
                fail_silently=False,
            )

        return response

    def get_success_url(self):
        return reverse('report:list_reports')

