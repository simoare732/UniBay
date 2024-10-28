from django.db import models

class Favourite(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='watchlist')
    product = models.ForeignKey('listings.Product', on_delete=models.CASCADE, related_name='watchlist')
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f'{self.user.username} - {self.product.title}'