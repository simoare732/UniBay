from django.db import models

class Review(models.Model):
    product = models.ForeignKey('listings.Product', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    rating = models.IntegerField() #Value between 1 and 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'user']

    def __str__(self):
        return f'{self.product.title} - {self.user.username}'
