from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from listings.models import Category
from .models import Favourite
from listings.models import Product

@login_required()
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




class list_favourites(ListView):
    model = Favourite
    template_name = 'watchlist/list_favourites.html'
    #ordering = ['-date']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()

        context['favourites'] = Favourite.objects.filter(user=self.request.user)

        return context

