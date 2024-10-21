from django.db import models

class Review(models.Model):
    product = models.ForeignKey('listings.Product', on_delete=models.CASCADE, related_name='reviews')
    reg_user = models.ForeignKey('users.Registered_User', on_delete=models.CASCADE, related_name='product_reviews')
    title = models.CharField(max_length=100)
    rating = models.IntegerField() #Value between 1 and 5
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        unique_together = ['product', 'reg_user']

    def __str__(self):
        return f'{self.product.title} - {self.reg_user.user.username}'


class Seller_Review(models.Model):
    reg_user = models.ForeignKey('users.Registered_User', on_delete=models.CASCADE, related_name='seller_reviews_by_user')
    seller = models.ForeignKey('users.Seller', on_delete=models.CASCADE, related_name='seller_reviews')
    title = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        unique_together = ['reg_user', 'seller']

    def __str__(self):
        return f'{self.reg_user.user.username} - {self.seller.user.username}'
