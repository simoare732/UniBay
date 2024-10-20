# Generated by Django 5.1.1 on 2024-10-20 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0007_product_sold_alter_product_image1'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='users.seller'),
        ),
    ]