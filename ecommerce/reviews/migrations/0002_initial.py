# Generated by Django 5.1.1 on 2024-10-21 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reviews', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='reg_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='users.registered_user'),
        ),
        migrations.AddField(
            model_name='seller_review',
            name='reg_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_reviews', to='users.registered_user'),
        ),
        migrations.AddField(
            model_name='seller_review',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_reviews_by_user', to='users.seller'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('product', 'reg_user')},
        ),
        migrations.AlterUniqueTogether(
            name='seller_review',
            unique_together={('reg_user', 'seller')},
        ),
    ]
