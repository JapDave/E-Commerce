from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from .models import Enterprise,Categories,Products
from .tasks import mail_sender_newenterprise
import hashlib


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
        mail_sender_newenterprise.delay(instance.enterprise_email,instance.enterprise_password)

        instance.enterprise_password = hashlib.sha256(str.encode(instance.enterprise_password)).hexdigest()
        super(Enterprise, instance).save()
