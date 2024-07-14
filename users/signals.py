from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import AddCredit


@receiver(post_save, sender=AddCredit)
def send_credit_added_email(sender, instance, created, **kwargs):
    if created:
        subject = 'New Credit Added'
        message = f'User {instance.user} added credit of amount {instance.amount} on {instance.timestamp}.'
        recipient_list = [admin_email for _, admin_email in settings.ADMINS]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        

