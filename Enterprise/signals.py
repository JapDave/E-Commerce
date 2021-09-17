from django.db.models.signals import post_save,pre_init
from django.dispatch import receiver
from .models import *
from django.conf import settings
from django.core.mail import send_mail

# @receiver(post_save, sender=Enterprise_Detail)
# def notify_user(sender, instance, created, **kwargs):
#     print('Entered')
#     if created:
#             subject = 'Hello'
#             message = 'Email sent succesfully by admin'
#             email_from = settings.EMAIL_HOST_USER
#             print(email_from)
#             recepient  = [instance.enterprise_email,]
#             print(recepient)
           # send_mail(subject, message, email_from, recepient)
    

