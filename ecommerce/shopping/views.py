import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from listings.models import Category
from .models import *

def add_to_cart(request, product_id):
    try:
        user = request.user
        product = Product.objects.get(id=product_id)

        data = json.loads(request.body)
        quantity = int(data.get('quantity'))

        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = Cart_Item.objects.get_or_create(cart=cart, product=product)

        # Created is True if the object was created, False if it already existed
        if not created:
            cart_item.inc_quantity(quantity)
        else:
            cart_item.quantity = quantity
            cart_item.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Prodotto aggiunto al carrello!',
            'total_items': cart.total_items(),
        })

    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart not found'}, status=404)


class list_cart(ListView):
    model = Cart
    template_name = 'shopping/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # To get all the Categories for search bar
        context['categories'] = Category.objects.all()
        context['cart'] = get_object_or_404(Cart, user=self.request.user)

        return context


@require_POST
def update_cart_item_quantity(request, item_pk):
    try:
        item = Cart_Item.objects.get(pk=item_pk, cart__user=request.user)
        data = json.loads(request.body)
        action = data.get('action')

        # Incremenet or decrement the quantity of the item
        if action == "increment":
            item.inc_quantity(1)
        elif action == "decrement" and item.quantity > 1:
            item.inc_quantity(-1)
        elif (action == "decrement" and item.quantity == 1) or action == "delete":
            item.delete()
            return JsonResponse({
                'quantity': 0,
                'total_items': item.cart.total_items(),
                'total_price': float(item.cart.total_price()),
            })

        # Return the new quantity and the total items and price in the cart
        return JsonResponse({
            'quantity': item.quantity,
            'total_items': item.cart.total_items(),
            'total_price': item.cart.total_price(),
        })
    except Cart_Item.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)