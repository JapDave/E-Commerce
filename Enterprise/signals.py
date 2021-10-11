from django.db.models.signals import post_delete, post_save,pre_init,pre_delete
from django.dispatch import receiver
from .models import Enterprise,Categories,Products
from .tasks import mail_sender_newenterprise



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
    mail_sender_newenterprise.delay(instance.enterprise_email,instance.enterprise_password)
