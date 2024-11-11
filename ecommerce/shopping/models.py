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



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='In progress')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f'Order of {self.user.username}'


class Order_Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'


