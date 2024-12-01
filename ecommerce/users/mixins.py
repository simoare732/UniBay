from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from listings.models import Product

class reguser_required_mixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and is a registered user
        if not request.user.is_authenticated or not request.user.is_registered_user:
            return redirect('pages:home_page')

        u = self.get_object()
        # Check if the user is the owner of the object
        if u.user != request.user:
            return redirect('pages:home_page')
        return super().dispatch(request, *args, **kwargs)


class seller_required_mixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and is a seller
        if not request.user.is_authenticated or not request.user.is_seller:
            return redirect('pages:home_page')

        u = self.get_object()
        # Check if the user is the owner of the object
        if u.user != request.user:
            return redirect('pages:home_page')
        return super().dispatch(request, *args, **kwargs)


class admin_required_mixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and is a staff or superuser
        if not request.user.is_authenticated or not(self.request.user.is_staff or self.request.user.is_superuser):
            return redirect('pages:home_page')
        return super().dispatch(request, *args, **kwargs)


class reguser_general_mixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and is a registered user
        if not request.user.is_authenticated or not request.user.is_registered_user:
            return redirect('pages:home_page')
        return super().dispatch(request, *args, **kwargs)


class seller_general_mixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and is a seller
        if not request.user.is_authenticated or not request.user.is_seller:
            return redirect('pages:home_page')
        return super().dispatch(request, *args, **kwargs)



class review_owner_mixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and is a registered user
        if not request.user.is_authenticated or not request.user.is_registered_user:
            raise Http404("Page not found")

        r = self.get_object()
        # Check if the user is the owner of the review
        if r.reg_user != request.user.registered_user:
            raise Http404("Page not found")
        return super().dispatch(request, *args, **kwargs)


class product_owner_mixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and is a seller
        if not request.user.is_authenticated or not request.user.is_seller:
            return redirect('pages:home_page')

        p = self.get_object()
        # Check if the seller is the owner of the product
        if p.seller != request.user.seller:
            return redirect('pages:home_page')
        return super().dispatch(request, *args, **kwargs)


class question_owner_mixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated and is a registered user
        if not request.user.is_authenticated or not request.user.is_seller:
            return redirect('pages:home_page')

        product_pk = self.kwargs.get('pk')
        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            return redirect('pages:home_page')

        # Check if the user is the owner of the product
        if product.seller != request.user.seller:
            return redirect('pages:home_page')

        return super().dispatch(request, *args, **kwargs)
