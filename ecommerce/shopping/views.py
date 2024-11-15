import json
from audioop import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, FormView, TemplateView

from listings.models import Category
from .models import *
from .forms import shipping_form, payment_form

@require_POST
def add_to_cart(request, product_id):
    try:
        user = request.user
        product = Product.objects.get(id=product_id)

        data = json.loads(request.body)
        quantity = data.get('quantity')

        if not quantity.isdigit() or int(quantity) < 1 or int(quantity) > product.quantity:
            return JsonResponse({
                'status': 'error',
            })

        quantity = int(quantity)

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
        max = item.product.quantity

        # Incremenet or decrement the quantity of the item
        if action == "increment" and item.quantity < max:
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


def order_success(request):
    categories = Category.objects.all()
    return render(request, 'shopping/order_success.html', {'categories': categories})


class checkout_view(TemplateView):
    template_name = 'shopping/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_id = self.request.GET.get('product_id')

        # If `product_id` is present, add only that product to the checkout, otherwise add all the items in the cart
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            quantity = self.request.GET.get('quantity')
            total_price = product.price * int(quantity)
            items = [{'product': product, 'quantity': quantity, 'total_price': total_price}]
            context['product_id'] = product_id

        else:
            cart = self.request.user.cart
            # Take all the items in the cart with their quantity and total price
            items = [{'product': item.product, 'quantity': item.quantity, 'total_price': item.total_price()} for item in cart.items.all()]
            total_price = cart.total_price()
            context['product_id'] = None

        context['total_price'] = total_price
        context['items'] = items

        context['shipping_form'] = kwargs.get('shipping_form', shipping_form())
        context['payment_form'] = kwargs.get('payment_form', payment_form())

        return context


    def post(self, request, *args, **kwargs):
        shipping_form_instance = shipping_form(request.POST)
        payment_form_instance = payment_form(request.POST)



        if shipping_form_instance.is_valid() and payment_form_instance.is_valid():
            # Create or get the Shipping and Payment instances. If shipping already exists, created_sh is False, otherwise True
            # Same with Payment
            with transaction.atomic():
                sh, created_sh = Shipping.objects.get_or_create(
                    country=shipping_form_instance.cleaned_data['country'],
                    name=shipping_form_instance.cleaned_data['name'],
                    surname=shipping_form_instance.cleaned_data['surname'],
                    shipping_address=shipping_form_instance.cleaned_data['shipping_address'],
                    city=shipping_form_instance.cleaned_data['city'],
                    zip_code=shipping_form_instance.cleaned_data['zip_code'],
                )
                pay, created_pay = Payment.objects.get_or_create(
                    card_number=payment_form_instance.cleaned_data['card_number'],
                    expiration_date=payment_form_instance.cleaned_data['expiration_date'],
                    cvv=payment_form_instance.cleaned_data['cvv'],
                )

                product_id = request.GET.get('product_id')

                if product_id:
                    product = get_object_or_404(Product, pk=product_id)
                    items = [{'product': product, 'quantity': int(request.GET.get('quantity', 1)), 'total_price': product.price}]
                    total_price = product.price

                else:
                    cart = request.user.cart
                    items = [{'product': item.product, 'quantity': item.quantity, 'total_price': item.total_price()} for
                             item in cart.items.all()]
                    total_price = cart.total_price()
                    # Empty the cart
                    cart.items.all().delete()

                order = Order.objects.create(
                    user=request.user,
                    status='Paid',
                    total_price=total_price,
                    shipping=sh,
                    payment=pay,
                )

                for item in items:
                    Order_Item.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        price=item['total_price'],
                    )

            return redirect('shopping:order_success')

        else:
            return self.render_to_response(
                self.get_context_data(shipping_form=shipping_form_instance, payment_form=payment_form_instance))