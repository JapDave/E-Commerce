from django.db.models.signals import post_delete, post_save,pre_init,pre_delete
from django.dispatch import receiver
from .models import *
from django.conf import settings
from django.core.mail import send_mail





@receiver(pre_delete, sender=Users, dispatch_uid='soft_delete_product')
def delete_product(sender, instance, **kwargs):
    cart_data = Cart.objects.filter(user=instance)
    for obj in cart_data:
        obj.delete()



@receiver(post_save, sender=Users)
def notify_user(sender, instance, created, **kwargs):
    if created:
            cart_data = Cart(user=instance)
            cart_data.save()

            subject = 'New Account Registered'
            message = f''' Thank-you for registering into our site.
            Your Login link : http://127.0.0.1:8000/user/login .
            '''
            email_from = settings.EMAIL_HOST_USER
            recepient  = [instance.user_email,]
            send_mail(subject, message, email_from, recepient)
    