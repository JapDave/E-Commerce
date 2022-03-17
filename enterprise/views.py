from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from .models import *
from user.models import Cart, Order
from .forms import ProductForm, EnterpriseForm
from django.conf import settings
from django.core.mail import send_mail,BadHeaderError
import random
from django.template.loader import render_to_string
from .tasks import mail_user_updateorder
import hashlib
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



class password_reset_request(View):

    def get(self,request):
         password_reset_form = PasswordResetForm()
         return render(request=request, template_name="password_reset.html", context={"form":password_reset_form})
   
    def post(self,request):
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "password_reset_email.txt"
                        c = {
                        "email":user.email,
                        'domain':'shopfreeapp.herokuapp.com',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        return redirect ("/password_reset/done/")
        
                else:
                    messages.error(request,'Sorry User Not Found')        
                    password_reset_form = PasswordResetForm()
                    return render(request=request, template_name="password_reset.html", context={"form":password_reset_form})




def is_authenticate(request):
    if request.session.get('enterprise_key'):
         return True
    return False


class ForgotPassword(View):
    def get(self, request):
        return render(request, 'email_verification.html')

    def post(self, request):
        user_email = request.POST['email']

        try:
            enterprise_data = Enterprise.objects.get(
                enterprise_email=user_email)
            request.session['temp_data'] = str(enterprise_data._id)
            generated_otp = random.randint(1111, 9999)
            request.session['otp'] = generated_otp
            subject = 'Acount Recovery'
            message = f'''your otp for account recovery is {generated_otp}'''
            email_from = settings.EMAIL_HOST_USER
            recepient = [user_email, ]
            send_mail(subject, message, email_from, recepient)
            return redirect(reverse('otp_verification'))

        except:
            messages.error(request, 'Email id not found try again.')
            return redirect(reverse('forgot_password'))


class OtpVerification(View):
    def get(self, request):
        return render(request, 'otp.html')

    def post(self, request):
        user_otp = request.POST['otp']
        if user_otp == str(request.session.get('otp')):
            return redirect(reverse('change_password'))
        else:
            messages.error(request, 'Wrong otp try again.')
            return redirect(reverse('otp_verification'))


class ChangePassword(View):
    def get(self, request):
        return render(request, 'change_password.html')

    def post(self, request):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            enterprise_id = request.session.get('temp_data')
            enterprise_data = Enterprise.objects.get(_id=enterprise_id)
            enterprise_data.enterprise_password = hashlib.sha256(
                str.encode(confirm_password)).hexdigest()
            enterprise_data.save()
            del request.session['temp_data']
            del request.session['otp']
            return redirect(reverse('enterprise_login'))
        else:
            messages.error(request, 'Password does not match.')
            return redirect(reverse('change_password'))


class Login(View):
    def get(self, request):
        rendered_data = {
            'title': 'Enterprise-login',
            'header': 'Enterprise'
        }
        return render(request, 'login.html', rendered_data)

    def post(self, request):
        user_mail = request.POST['usermail']
        user_password = request.POST['password']
        try:
            fetched_data = Enterprise.objects.filter(
                enterprise_email=user_mail).first()
            if fetched_data != None and hashlib.sha256(str.encode(user_password)).hexdigest() == fetched_data.enterprise_password:
                request.session['enterprise_key'] = str(fetched_data._id)
                return redirect(reverse('enterprise_index'))
            else:
                raise ValueError()
        except ValueError:
            messages.error(request, 'wrong username or password')
            return redirect(reverse('enterprise_login'))
        except Exception as e:
            messages.error(request, 'something went wrong try again')
            return redirect(reverse('enterprise_login'))


class Logout(View):
    def get(self, request):
        if is_authenticate(request):
            del request.session['enterprise_key']
        return redirect(reverse('enterprise_login'))


class Profile(View):
    def get(self, request):
        if is_authenticate(request):
            enterprise_data = Enterprise.objects.filter(
                _id=request.session.get('enterprise_key')).first()
            form = EnterpriseForm(instance=enterprise_data)
            return render(request, 'enterprise/profile.html', {'form': form})
        else:
            return redirect(reverse('enterprise_login'))

    def post(self, request):
        enterprise_data = Enterprise.objects.filter(
            _id=request.session.get('enterprise_key')).first()
        form = EnterpriseForm(request.POST, request.FILES,
                              instance=enterprise_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile is updated successfully')
            return redirect(reverse('enterprise_profile'))
        else:
            messages.success(request, 'Your Profile is not updated')
            return render(request, 'enterprise/profile.html', {'form': form})


class ProfileChangePassword(View):
	def get(self, request):
		if request.session.get('enterprise_key'):
			return render(request, 'profile_change_password.html')
		else:
			return redirect(reverse('login'))

	def post(self, request):

		old_password = request.POST['old_password']
		password = request.POST['new_password']
		confirm_password = request.POST['confirm_password']
		if password == confirm_password:
			try:
				user_data = Enterprise.objects.get(_id=request.session.get('enterprise_key'))
				if hashlib.sha256(str.encode(old_password)).hexdigest() == user_data.enterprise_password:
					user_data.enterprise_password = hashlib.sha256(str.encode(confirm_password)).hexdigest()
					user_data.save()
					messages.error(request,'Password Has Successfully Changed')
					return redirect(reverse('enterprise_profile'))
				else: 
					messages.error(request,'Sorry Password not found')
					return redirect(reverse('profile_enterprise_change_password'))
			except:
				messages.error(request,'Sorry Password Not Updated Try Again ')
				return redirect(reverse('profile_enterprise_change_password'))
		else:
			messages.error(request,'Password does not match.')
			return redirect(reverse('profile_enterprise_change_password'))


class Index(View):
    def get(self, request):
        try:
            if is_authenticate(request):
                enterprise_data = Enterprise.objects.filter(_id = request.session.get('enterprise_key')).first()
                rendered_data = {
                    'enterprise_name': enterprise_data.enterprise_name,
                }
                return render(request,'enterprise/index.html',rendered_data)
            else:
                return redirect(reverse('enterprise_login'))
        except:
            messages.error(request,"Sorry Could'nt Login Try Again.")
            return redirect(reverse('enterprise_login'))

           
class ProductsList(View):
    def get(self, request):
        if is_authenticate(request):
            products_data  = Products.objects.filter(product_enterprsie = request.session.get('enterprise_key'))
            rendered_data = {
                'products': products_data,         
            }
            return render(request,'enterprise/list_products.html',rendered_data)
        else:
            return redirect(reverse('enterprise_login'))

    def post(self,request):
        selected_action = request.POST.get( 'actions')
        selected_item = request.POST.getlist('products')
        if selected_item == [] or selected_action == None:
            messages.error(request,'please select item and the prefered action to perform.')
            return redirect(reverse('product_list'))
        else:
            deleted_product = Products.objects.filter(_id__in=selected_item)
            deleted_product.delete()
            cart_data = Cart.objects.filter(product_items___id__in = selected_item)
            cart_data.delete()
            return redirect(reverse('product_list'))

class AddProduct(View):
    def get(self,request):
        if is_authenticate(request):
            enterprise_data = Enterprise.objects.filter(_id = request.session.get('enterprise_key')).first()
            form=ProductForm(initial={'product_enterprsie': enterprise_data})
            rendered_data = {
                'enterprise':enterprise_data,
                'form':form
            }
            return render(request,'enterprise/add_product.html',rendered_data)
        else:
            return redirect(reverse('enterprise_login'))

    def post(self,request):
            form = ProductForm(request.POST,request.FILES)    
            if form.is_valid():
                    form.save()
                    messages.success(request,'Product Added Successfully.')
                    return redirect(reverse('product_list'))
            else:
                return render(request,'enterprise/add_product.html',{'form':form})
               
class UpdateProduct(View):

    def get(self,request,id):
        product_data = Products.objects.get(_id = id)
        if is_authenticate(request):   
            form = ProductForm(instance=product_data)
            rendered_data = {
                'form':form
            }
            return render(request,'enterprise/update_product.html',rendered_data)
        else:
            return redirect(reverse('enterprise_login'))

    def post(self,request,id):
            product_data = Products.objects.get(_id=id)
            form = ProductForm(request.POST,request.FILES,instance=product_data)
            
            if request.POST.get('save'):
                if form.is_valid():
                    form.save()
                    return redirect(reverse('product_list'))
                else:
                    render(request,'enterprise/add_product.html',{'form':form})
            
            elif request.POST.get('delete'):
                product_data.delete()
                return redirect(reverse('product_list'))

class DeleteProduct(View):
    def get(self,request,id):
        if is_authenticate(request):
            product_data = Products.objects.get(_id=id)
            product_data.delete()
            return redirect(reverse('product_list'))
        else:
            return redirect(reverse('enterprise_login'))

class OrderRequest(View):
    def get(self,request):
        if is_authenticate(request):
            order_data = Order.objects.filter(product__product_enterprsie = request.session.get('enterprise_key'))
            return render(request,'enterprise/list_orders.html',{'products':order_data})
        else:
            return redirect(reverse('enterprise_login'))


class OrderDetail(View):
    def get(self,request,id):
        if is_authenticate(request):
            order_data = Order.objects.get(_id=id)
            return render(request,'enterprise/order_detail.html',{'order':order_data})
        else:
            return redirect(reverse('enterprise_login'))


    def post(self,request,id):
        order_data = Order.objects.get(_id=id)
        status = request.POST['order_status']
        order_data.status = status
        order_data.save()
        if order_data.status == '1':
            mail_user_updateorder.delay(status,order_data.user.user_email,order_data.product._id)
        elif order_data.status == '2':
            mail_user_updateorder.delay(status,order_data.user.user_email,order_data.product._id)
        elif order_data.status =='3':
            mail_user_updateorder.delay(status,order_data.user.user_email,order_data.product._id)
        elif order_data.status == '4':
            mail_user_updateorder.delay(status,order_data.user.user_email,order_data.product._id)

        product_data = Products.objects.get(_id=order_data.product._id)
        product_data.product_qty -= order_data.qty
        product_data.save()
        return render(request,'enterprise/order_detail.html',{'order':order_data})

