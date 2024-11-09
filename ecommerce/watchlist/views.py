from ctypes.wintypes import POINT

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from listings.models import Category
from .models import Favourite
from listings.models import Product

@require_POST # It accepts only POST requests
def toggle_favorite(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    favorite, created = Favourite.objects.get_or_create(user=user, product=product)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})


@login_required(login_url='users:login')
def remove_favorite(request, favorite_id):
    try:
        favorite = Favourite.objects.get(id=favorite_id)
        favorite.delete()  # Rimuovi l'elemento dai preferiti
        return JsonResponse({'success': True})
    except Favourite.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'not_favorite'}, status=400)

class list_favourites(LoginRequiredMixin, ListView):
    model = Favourite
    template_name = 'watchlist/list_favourites.html'
    paginate_by = 10

    login_url = 'users:login'

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()


        return context

