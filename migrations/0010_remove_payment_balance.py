# Generated by Django 3.2.18 on 2024-07-12 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_classified', '0009_payment_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='balance',
        ),
    ]
