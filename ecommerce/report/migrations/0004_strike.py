# Generated by Django 5.1.1 on 2024-11-03 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_alter_report_unique_together'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Strike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='strikes', to='users.seller')),
            ],
        ),
    ]
