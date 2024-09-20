from django.db import models
from django.contrib.auth.models import User

#Class Profile that allows to create a profile for each user
class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('CLIENTE', 'Cliente'),
        ('VENDITORE', 'Venditore'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='CLIENTE')
    nome = models.CharField(max_length=50, blank=True)
    cognome = models.CharField(max_length=50, blank=True)
    partita_iva = models.CharField(max_length=20, blank=True)
    email_aziendale = models.EmailField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
