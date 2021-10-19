from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from .models import Users,Cart  
from .tasks import mail_sender_newuser
import hashlib


@receiver(pre_delete, sender=Users, dispatch_uid='soft_delete_product')
def delete_product(sender, instance, **kwargs):
    cart_data = Cart.objects.filter(user=instance)
    for obj in cart_data:
        obj.delete()


@receiver(post_save, sender=Users)
def notify_user(sender, instance, created, **kwargs):
    if created:
        mail_sender_newuser.delay(instance.user_email)
    
        instance.user_password = hashlib.sha256(str.encode(instance.user_password)).hexdigest()
        super(Users, instance).save()


