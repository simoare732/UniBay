# Generated by Django 5.1.1 on 2024-11-02 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='reason',
            field=models.CharField(choices=[('SP', 'Spam'), ('TR', 'Truffa'), ('IN', 'Inappropriato'), ('AL', 'Altro')], max_length=2),
        ),
    ]
