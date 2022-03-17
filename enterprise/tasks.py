from enterprise.models import Products
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task(name='mail_sender_newenterprise')
def mail_sender_newenterprise(email,password):
     
   subject = 'New Account Registered'
   message = f''' Thank-you for registering into our site.
   Your Login link : https://shopfreeapp.herokuapp.com/enterprise/ .
   username : {email}.
   password: {password}.'''

   email_from = settings.EMAIL_HOST_USER
   recepient  = [email,]
   send_mail(subject, message, email_from, recepient)
              
    

@shared_task(name='mail_user_updatedorder')
def mail_user_updateorder(status,email,id):
   product = Products.objects.get(_id=id)
   if status == '1':

      subject = 'Product Order Approved'
      message = f''' Your Product {product.product_name} is approved and soon will be dispatched.'''

      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)

   elif status == '2':
      subject = 'Product Order Dispatched'
      message = f''' Your Product {product.product_name} is Dispatched and soon will be delivered.'''

      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)

   elif status == '3':
      subject = 'Product Order Delivered'
      message = f''' Your Product {product.product_name} is Delivered to the Location given.'''

      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)

   elif status ==  '4':
      subject = 'Product Order Cancelled'
      message = f''' Your Product {product.product_name} is Cancelled your transaction will be rolled back.'''

      email_from = settings.EMAIL_HOST_USER
      recepient  = [email,]
      send_mail(subject, message, email_from, recepient)
