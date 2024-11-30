from django.db import models
from users.models import User
from listings.models import Product

# This represents the cart of a user
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'Cart of {self.user.username}'

    def total_price(self):
        t = 0
        for item in self.items.all():
            t = t + item.total_price()
        return t

    def total_items(self):
        c = 0
        for item in self.items.all():
            c = c + item.quantity
        return c

# This represents an item in the cart
class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f'Cart of {self.cart.user.username} - {self.quantity} of {self.product.title}'

    def inc_quantity(self, n):
        self.quantity = self.quantity + n
        self.save()

    def total_price(self):
        return self.quantity * self.product.price


# This represents an order of a user
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='In progress')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, null=False)
    shipping = models.ForeignKey('Shipping', on_delete=models.CASCADE, null=True, blank=True, related_name='order')
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True, related_name='order')

    def __str__(self):
        return f'Order of {self.user.username}, n° {self.pk}'

    def order_shipped(self):
        self.status = 'Shipped'
        self.save()

    def order_delivered(self):
        self.status = 'Delivered'
        self.save()

    def order_paid(self):
        self.status = 'Paid'
        self.save()

# This represents an item in an order
class Order_Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    status = models.CharField(max_length=20, default='In progress')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} of {self.product.title} in order n° {self.order.pk}'


    def item_shipped(self):
        self.status = 'Shipped'
        self.save()

        cart_sent = True

        for item in self.order.items.all():
            if item.status == 'Paid' or item.status == 'In progress':
                cart_sent = False
                break

        if cart_sent:
            self.order.order_shipped()

        self.save()

    def item_delivered(self):
        self.status = 'Delivered'

        cart_delivered = True

        for item in self.order.items.all():
            if item.status != 'Delivered':
                cart_delivered = False
                break

        if cart_delivered:
            self.order.order_delivered()

        self.save()


# This represents the shipping information of an order
class Shipping(models.Model):
    country = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20, null=False)
    surname = models.CharField(max_length=20, null=False)
    shipping_address = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=50, null=False)
    zip_code = models.CharField(max_length=5, null=False)


    def __str__(self):
        return f'Address of {self.name} {self.surname} in {self.city}'


# This represents the payment information of an order
class Payment(models.Model):
    # In a real application, we would use a more secure way to store credit card information
    card_number = models.CharField(max_length=16, null=False)
    expiration_date = models.CharField(max_length=5, null=False)
    cvv = models.CharField(max_length=4, null=False)

    def __str__(self):
        return f'Payment with card ending in {self.card_number[-4:]}'