from django.db import models

class Review(models.Model):
    product = models.ForeignKey('listings.Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='product_reviews')
    title = models.CharField(max_length=100)
    rating = models.IntegerField() #Value between 1 and 5
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        unique_together = ['product', 'user']

    def __str__(self):
        return f'{self.product.title} - {self.user.username}'


class Seller_Review(models.Model):
    seller = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='seller_reviews')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='seller_reviews_by_user')
    title = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        unique_together = ['seller', 'user']

    def __str__(self):
        return f'{self.seller.username} - {self.user.username}'
