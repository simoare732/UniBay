from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    is_registered_user = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

class Registered_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    PIVA = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        # Delete all products of the seller
        for product in self.products.all():
            product.delete()
        super().delete(*args, **kwargs)
