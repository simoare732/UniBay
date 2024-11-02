from django.db import models

class Report(models.Model):
    reason_choices = [
        ('SP', 'Spam'),
        ('TR', 'Truffa'),
        ('IN', 'Inappropriato'),
        ('AL', 'Altro')
    ]

    reporter = models.ForeignKey('users.Registered_User', on_delete=models.CASCADE, related_name='reports')
    seller = models.ForeignKey('users.Seller', on_delete=models.CASCADE, related_name='reports')
    reason = models.CharField(max_length=2, choices=reason_choices)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    def __str__(self):
        return f'Report di {self.reporter.user.username} verso {self.seller.user.username}'

    # Get the reason of the report in extense form
    def get_reason(self):
        return dict(self.reason_choices)[self.reason]