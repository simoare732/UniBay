from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages

class registered_user_required_mixin(LoginRequiredMixin):
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