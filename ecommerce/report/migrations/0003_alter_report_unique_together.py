# Generated by Django 5.1.1 on 2024-11-03 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_alter_report_reason'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together={('reporter', 'seller')},
        ),
    ]
