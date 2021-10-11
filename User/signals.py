from django.db.models.signals import post_delete, post_save,pre_init,pre_delete
from django.dispatch import receiver
from .models import *
from .tasks import mail_sender_newuser




@receiver(pre_delete, sender=Users, dispatch_uid='soft_delete_product')
def delete_product(sender, instance, **kwargs):
    cart_data = Cart.objects.filter(user=instance)
    for obj in cart_data:
        obj.delete()


@receiver(post_save, sender=Users)
def notify_user(sender, instance, created, **kwargs):
    mail_sender_newuser.delay(instance.user_email)


