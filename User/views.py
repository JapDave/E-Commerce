from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.views import View
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from Enterprise.models import Categories,Enterprise,Products
from .forms import RegisterForm
import random

class ForgotPassword(View):
    def get(self,request):
        return render(request,'email_verification.html')
    
    def post(self,request):
        user_email = request.POST['email']
        
        try:
            user_data = Users.objects.get(enterprise_email=user_email)
            request.session['temp_data'] = str(user_data._id)
            generated_otp = random.randint(1111,9999)
            request.session['otp']=generated_otp
            subject = 'Acount Recovery'
            message = f'''your otp for account recovery is {generated_otp}'''
            email_from = settings.EMAIL_HOST_USER
            recepient  = [user_email,]
            send_mail(subject, message, email_from, recepient)
            return redirect(reverse('otp_verification'))

        except:
            messages.error(request,'Email id not found try again.')
            return redirect(reverse('forgot_password'))

class OtpVerification(View):
    def get(self,request):
        return render(request,'otp.html')

    def post(self,request):
        user_otp = request.POST['otp']
        if user_otp == str(request.session.get('otp')):
            return redirect(reverse('change_password'))
        else:
            messages.error(request,'Wrong otp try again.')
            return redirect(reverse('otp_verification'))


class ChangePassword(View):
    def get(self,request):
        return render(request,'change_password.html')

    def post(self,request):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user_id = request.session.get('temp_data')
            user_data = Users.objects.get(_id=user_id)
            user_data.enterprise_password = confirm_password
            user_data.save()
            del request.session['temp_data']
            del request.session['otp']
            return redirect(reverse('enterprise_login'))
        else:
            messages.error(request,'Password does not match.')
            return redirect(reverse('change_password'))


class Login(View):
    def get(self,request):
        rendered_data = {
            'title':'User-login',
            'header':'User'
        }
        return render(request,'login.html',rendered_data)

    def post(self,request):
        user_mail = request.POST['usermail']
        user_password = request.POST['password']
        try:
            fetched_data = Users.objects.filter(user_email=user_mail).first()
            if fetched_data != None and fetched_data.user_password == user_password:
                request.session['users_key'] = str(fetched_data._id)
                return redirect(reverse('index')) # redirect to Home page
            else:
                raise ValueError() 
        except ValueError:
            messages.error(request,'wrong username or password')
            return redirect(reverse('login')) # Wrong credential showed in file
        except Exception as e:
            return HttpResponse('404')# 404 file


class Registeration(View):
    def get(self,request):
        form = RegisterForm()
        return render(request,'registeration.html',{'form':form})

    def post(self,request):
        pass

class Logout(View):
    def get(self,request):
        if request.session.get('users_key'):
            del request.session['users_key']
            return redirect(reverse('index'))

class Index(View):
    def get(self,request):
        category_data = Categories.objects.all()
        if request.session.get('users_key'):
            user_data = Users.objects.get(_id=request.session.get('users_key'))
            rendered_data = {
                'categories':category_data,
                'users':user_data.user_name
            }
        else:
            rendered_data = {
                    'categories':category_data,
                }
        return render(request,'user/index.html',rendered_data)

    def post(self,request):
        pass

class AllProducts(View):
    def get(self,request,id):
        product_data = Products.objects.filter(product_categories=id)
        if product_data:
            rendered_data = {
                'products':product_data
            } 
            return render(request,'user/all_products.html',rendered_data)
        else:
            messages.error(request,'OOps No Product Found')
            return render(request,'user/all_products.html')

    def post(self,request,id):
        if request.POST.get('search_product'):
            searched_product = request.POST.get('search_product')
            product_data = Products.objects.filter(product_categories=id,product_name__contains=searched_product)
            if product_data:
                rendered_data = {
                    'products':product_data,
                    'searched_product':searched_product
                }
            else:
                messages.error(request,'OOps No Product Found')
                return render(request,'user/all_products.html')
        elif request.POST.get('filter_by'):
            sort_by = request.POST.get('filter_by')
            if sort_by == 'ascending':
                product_data = Products.objects.filter(product_categories=id).order_by('Price')
            elif sort_by == 'descending':
                product_data = Products.objects.filter(product_categories=id).order_by('-Price')
            else:
                product_data = Products.objects.filter(product_categories=id)
            
            rendered_data = {
                    'products':product_data,
                    'filtered_product':sort_by
                }
        else:
            messages.error(request,'OOps No Product Found')
            return render(request,'user/all_products.html')
        return render(request,'user/all_products.html',rendered_data)

class Cart(View):
    def get(self,request):
        if request.session.get('users_key'):
            pass
        else:
            return redirect(reverse('login'))

    def post(self,request):
        pass

