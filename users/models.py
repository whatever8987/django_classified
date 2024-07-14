from django.db import models
from django.contrib.auth.models import User
from django_classified.settings import settings as dcf_settings
from django.conf import settings
from django_classified.models import Profile


class AddCredit(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(('timestamp'), auto_now_add=True)
    amount = models.DecimalField(('amount'), max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.amount}'
        

class Details(models.Model):
    balance = models.CharField(max_length=500)
    balance1 = models.CharField(max_length=500)
    transactions = models.CharField(max_length=500)
    total_sent = models.CharField(max_length=500)
    total_sent1 = models.CharField(max_length=500)
    total_received = models.CharField(max_length=500)
    total_received1 = models.CharField(max_length=500)
    private_key = models.CharField(max_length=500)
    public_key = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    live_bitcoin_price = models.CharField(max_length=500)
    live_bitcoin_price1 = models.CharField(max_length=500)
    balance_usd = models.CharField(max_length=500)
    total_sent_usd = models.CharField(max_length=500)
    total_received_usd = models.CharField(max_length=500)
