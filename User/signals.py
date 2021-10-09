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
            # cart_data = Cart(user=instance)
            # cart_data.save()

            subject = 'New Account Registered'
            message = f''' Thank-you for registering into our site.
            Your Login link : http://127.0.0.1:8000/user/login .
            '''
            email_from = settings.EMAIL_HOST_USER
            recepient  = [instance.user_email,]
            send_mail(subject, message, email_from, recepient)


@receiver(post_save, sender=Order)
def notify_user(sender, instance, created, **kwargs):
    if created:
        # subject = 'Order Placed'
        # message = f''' Thank-you for placing order,your package will be delievered soon.
        # Order Details are as follow-
        # Order-id - {str(instance._id)}
        # Product- {instance.product.product_name}
        # qty - {instance.qty}
        # paid Amount - {instance.total}
        # Address - {instance.address}
        
        # For any inquiry feel free to contact.
        # Thank you
        # Keep Shopping 
        # '''
        # email_from = settings.EMAIL_HOST_USER
        # recepient  = [instance.user.user_email,]
        # send_mail(subject, message, email_from, recepient)
       
    
        subject = 'Order Recieved'
        message = f''' An Order for an product for your enterprise is been recieved please check for status.
        Order Details are as follow- 
        product- {instance.product.product_name}
        qty - {instance.qty}
      
        
        Customer Details are as follow-
        Name - {instance.user.user_name}
        contact - {instance.user.user_contact}
        Address - {instance.address}

        For any inquiry feel free to contact.
        Thank you
        '''
        email_from = settings.EMAIL_HOST_USER
        recepient  = [instance.product.product_enterprsie.enterprise_email,]

        send_mail(subject, message, email_from, recepient)
       
      
       