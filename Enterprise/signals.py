from django.db.models.signals import post_delete, post_save,pre_init,pre_delete
from django.dispatch import receiver
from .models import *
from django.conf import settings
from django.core.mail import send_mail


@receiver(pre_delete, sender=Enterprise, dispatch_uid='soft_delete_product')
def delete_product(sender, instance, **kwargs):
    product_data = Products.objects.filter(product_enterprsie=instance)
    for obj in product_data:
        obj.delete()

@receiver(pre_delete, sender=Categories, dispatch_uid='soft_delete_product')
def delete_product(sender, instance, **kwargs):
    product_data = Products.objects.filter(product_categories=instance)
    for obj in product_data:
        obj.delete()



@receiver(post_save, sender=Enterprise)
def notify_user(sender, instance, created, **kwargs):
    if created:
            subject = 'New Account Registered'
            message = 'http://127.0.0.1:8000/enterprise/'
            email_from = settings.EMAIL_HOST_USER
            recepient  = [instance.enterprise_email,]
            send_mail(subject, message, email_from, recepient)
    



