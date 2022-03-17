from celery import shared_task
from .models import Order
from django.conf import settings
from django.core.mail import send_mail



@shared_task(name='mail_sender_enterprise')
def mail_sender_enterprise(order_obj_id):
     
   order_obj = Order.objects.get(_id=order_obj_id)

   subject = 'Order Recieved'
   message = f''' An Order for an product for your enterprise is been recieved please check for status.
   Order Details are as follow- 
   product- {order_obj.product.product_name}
   qty - {order_obj.qty}

   
   Customer Details are as follow-
   Name - {order_obj.user.user_name}
   contact - {order_obj.user.user_contact}
   Address - {order_obj.address}

   For any inquiry feel free to contact.
   Thank you
   '''
   email_from = settings.EMAIL_HOST_USER
   recepient  = [order_obj.product.product_enterprsie.enterprise_email,]

   send_mail(subject, message, email_from, recepient)



@shared_task(name='mail_sender_user')
def mail_sender_user(order_no,user_email):
      subject = 'Order Placed'
      message = f''' Thank-you for placing order,your package will be delievered soon with
      Order No - {order_no} OR Check Out Details in Order History.
      For any inquiry feel free to contact.
      Thank you
      Keep Shopping 
      '''

      email_from = settings.EMAIL_HOST_USER
      recepient  = [user_email,]
      send_mail(subject, message, email_from, recepient)

    
@shared_task(name='mail_sender_newuser')
def mail_sender_newuser(email):

      subject = 'New Account Registered'
      message = f''' Thank-you for registering into our site.
      Your Login link : https://shopfreeapp.herokuapp.com/ .
      '''
      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)


