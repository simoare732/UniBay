import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from listings.models import Category
from .models import *
from .forms import *

@require_POST
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


class list_cart(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'shopping/cart.html'

    login_url = 'users:login'

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



class checkout_view(View):
    def get(self, request):
        product_id = request.GET.get('product_id')
        cart = request.user.cart
        form = address_form()

        # Se `product_id` è presente, aggiunge solo quel prodotto al checkout
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            total_price = product.price
            items = [{'product': product, 'quantity': 1, 'total_price': total_price}]
        else:
            # Altrimenti, aggiunge tutti gli articoli nel carrello
            items = [{'product': item.product, 'quantity': item.quantity, 'total_price': item.total_price()} for item in cart.items.all()]
            total_price = cart.total_price()

        return render(request, 'shopping/checkout.html', {
            'items': items,
            'form': form,
            'total_price': total_price,
            'single_product': bool(product_id),  # Passiamo questo valore al template
        })

    def post(self, request):
        product_id = request.GET.get('product_id')
        form = address_form(request.POST)
        if form.is_valid():
            # Se è presente un `product_id`, creiamo un ordine per quel singolo prodotto
            if product_id:
                product = get_object_or_404(Product, pk=product_id)
                total_price = product.price

                # Creazione dell'ordine
                order = Order.objects.create(
                    user=request.user,
                    status='In progress',
                    total_price=total_price,
                )

                # Aggiungi il prodotto come `Order_Item`
                Order_Item.objects.create(
                    order=order,
                    product=product,
                    quantity=1,
                    price=total_price,
                )

            else:
                # Altrimenti, creiamo un ordine per tutti gli articoli nel carrello
                cart = request.user.cart
                order = Order.objects.create(
                    user=request.user,
                    status='In progress',
                    total_price=cart.total_price(),
                )

                # Aggiungiamo ogni elemento del carrello all'ordine
                for item in cart.items.all():
                    Order_Item.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.total_price(),
                    )

                # Svuota il carrello
                cart.items.all().delete()

            # Redirect alla pagina di conferma dell'ordine
            return redirect('shopping:order_success')

        return render(request, 'shopping/checkout.html', {
            'error': 'Errore durante l’elaborazione del pagamento',
        })