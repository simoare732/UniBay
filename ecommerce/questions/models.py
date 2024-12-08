from django.db import models
from users.models import Registered_User, User
from listings.models import Product

class Question(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="questions")
    reg_user = models.ForeignKey(Registered_User, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return f"Question from {self.reg_user.user.username} about {self.product.title}"


    def is_answered(self):
        return self.answer.filter(approved=True).count() > 0

    def get_answer(self):
        return self.answer.filter(approved=True).first()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answer")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer")
    text = models.TextField()
    approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        unique_together = ['question', 'user']

    def __str__(self):
        return f"Answer to question from {self.question.reg_user.user.username} about {self.question.product.title}"



    def approve(self):
        self.approved = True
        self.save()

