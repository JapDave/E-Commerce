from django.db.models.aggregates import Sum
from .tasks import mail_sender_enterprise, mail_sender_user
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from .models import Users,Order,Cart,Address
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from enterprise.models import Categories,Products
from .forms import AddressForm, RegisterForm,ProfileForm
import random
from django.core.paginator import Paginator
from django.db.models import  Count
import hashlib

class Faqs(View):
	def get(self,request):
		if request.session.get('users_key'):
			return render(request,'user/faqs.html',{'users':True})
		else:
			return render(request,'user/faqs.html')

class Aboutus(View):
	def get(self,request):
		if request.session.get('users_key'):
			return render(request,'user/aboutus.html',{'users':True})
		else:
			return render(request,'user/aboutus.html')


class ForgotPassword(View):
	def get(self,request):
		return render(request,'user/email_verification.html')
	
	def post(self,request):
		user_email = request.POST['email']
		try:
			user_data = Users.objects.get(user_email=user_email)
			request.session['temp_data'] = str(user_data._id)
			generated_otp = random.randint(1111,9999)
			request.session['otp']=generated_otp	
			subject = 'Acount Recovery'
			message = f'''your otp for account recovery is {generated_otp}'''
			email_from = settings.EMAIL_HOST_USER
			recepient  = [user_email,]
			send_mail(subject, message, email_from, recepient)
			return redirect(reverse('user_otp_verification'))
		except:
			messages.error(request,'Email id not found try again.')
			return redirect(reverse('user_forgot_password'))


class OtpVerification(View):
	def get(self,request):
		return render(request,'user/otp.html')

	def post(self,request):
		user_otp = request.POST['otp']
		if user_otp == str(request.session.get('otp')):
			return redirect(reverse('user_change_password'))
		else:
			messages.error(request,'Wrong otp try again.')
			return redirect(reverse('user_otp_verification'))


class ChangePassword(View):
	def get(self,request):
		return render(request,'user/change_password.html')

	def post(self,request):
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']
		if password == confirm_password:
			user_id = request.session.get('temp_data')
			user_data = Users.objects.get(_id=user_id)
			user_data.user_password = hashlib.sha256(str.encode(confirm_password)).hexdigest()
			user_data.save()
			del request.session['temp_data']
			del request.session['otp']
			return redirect(reverse('login'))
		else:
			messages.error(request,'Password does not match.')
			return redirect(reverse('user_change_password'))


class Login(View):
	def get(self,request):
		return render(request,'user/login.html')

	def post(self,request):
		user_mail = request.POST['usermail']
		user_password = request.POST['password']
		try:
			fetched_data = Users.objects.filter(user_email=user_mail).first()
			if fetched_data != None and hashlib.sha256(str.encode(user_password)).hexdigest() == fetched_data.user_password :
				request.session['users_key'] = str(fetched_data._id)
				return redirect(reverse('index'))
			else:
				raise ValueError() 
		except ValueError:
			messages.error(request,'wrong username or password')
			return redirect(reverse('login')) 
		except:
			messages.error(request,'Login Failed Try Again')
			return redirect(reverse('login')) 


class Registeration(View):
	def get(self,request):
		user_form = RegisterForm()
		address_form = AddressForm()
		return render(request,'user/register.html',{'userform':user_form,'addressform':address_form})

	def post(self,request):
		user_form = RegisterForm(request.POST,request.FILES)
		address_form = AddressForm(request.POST,request.FILES)


		if user_form.is_valid:
			try:
				user_obj = user_form.save(commit=False)
				if user_obj:
					address_form.data._mutable = True
					address_form.data['user'] = user_obj
					address_form.data._mutable = False
					user_form.save()
					address_form.save()
				return redirect(reverse('login'))
			except Exception as e:
				return render(request,'user/register.html',{'userform':user_form,'addressform':address_form})
		else:
			return render(request,'user/register.html',{'userform':user_form,'addressform':address_form})
				

class Logout(View):
	def get(self,request):
		if request.session.get('users_key'):
			del request.session['users_key']
			del request.session['cart_count']
		return redirect(reverse('index'))


class Profile(View):
	def get(self,request):
		if request.session.get('users_key'):
			user_data = Users.objects.get(_id=request.session.get('users_key'))
			form = ProfileForm(instance=user_data)	
			return render(request,'user/profile.html',{'form':form,'users':user_data,'cart_count':request.session['cart_count'],'categories':Categories.objects.all()})
		else:
			return redirect(reverse('login'))

	def post(self,request):
		user_data = Users.objects.get(_id=request.session.get('users_key'))
		form = ProfileForm(request.POST,request.FILES,instance=user_data) 
	
		if request.POST.get('register'):
			if form.is_valid():
				form.save()
				messages.success(request,'Your Profile is updated successfully	')
				return redirect(reverse('user_profile'))
			
			else:
				messages.success(request,'Your Profile is not updated')
				return render(request,'user/profile.html',{'form':form,'users':True})
			

class ProfileChangePassword(View):
	def get(self,request):
		if request.session.get('users_key'):
			return render(request,'user/profile_change_password.html')
		else:
			return redirect(reverse('login'))

	def post(self,request):
		old_password = request.POST['old_password']
		password = request.POST['new_password']
		confirm_password = request.POST['confirm_password']
		if password == confirm_password:
			try:
				user_data = Users.objects.get(_id=request.session.get('users_key'))
				if hashlib.sha256(str.encode(old_password)).hexdigest() == user_data.user_password:
					user_data.user_password = hashlib.sha256(str.encode(confirm_password)).hexdigest()
					user_data.save()
					messages.error(request,'Password Has Successfully Changed')
					return redirect(reverse('user_profile'))
				else: 
					messages.error(request,'Sorry Password not found')
					return redirect(reverse('profile_user_change_password'))
			except:
				messages.error(request,'Sorry Password Not Updated Try Again ')
				return redirect(reverse('profile_user_change_password'))
		else:
			messages.error(request,'Password does not match.')
			return redirect(reverse('profile_user_change_password'))


class UserAddress(View):
	def get(self,request):
		if request.session.get('users_key'):
			address_data = Address.objects.filter(user___id = request.session.get('users_key'))
			cart_data = Cart.objects.filter(user___id = request.session.get('users_key'))

			rendered_data = {
				'users':True,
				'cart_count':cart_data.count(),
				'address':address_data
			}
			return render(request,'user/user_address.html',rendered_data)
		else:
			return redirect(reverse('login'))


class AddressDetail(View):
	def get(self,request,id):
		if request.session.get('users_key'):
			cart_data = Cart.objects.filter(user___id = request.session.get('users_key'))
		
			if id == 'newaddress':
				address_form = AddressForm()
				
			else:
				address_data = Address.objects.get(user___id = request.session.get('users_key'),_id=id)
				address_form = AddressForm(instance=address_data)
				
			rendered_data = {
				'users':True,
				'cart_count':cart_data.count(),
				'addressform':address_form
			}
			return render(request,'user/address_detail.html',rendered_data)
		else:
			return redirect(reverse('login'))

	def post(self,request,id):
		if request.session.get('users_key'):
			if id == 'newaddress':
				user_data = Users.objects.get(_id=request.session.get('users_key'))
				address_form = AddressForm(request.POST)
				address_form.data._mutable = True
				address_form.data['user'] = user_data
				address_form.data._mutable = False
			else:
				address_data = Address.objects.get(user___id = request.session.get('users_key'),_id=id)
				address_form = AddressForm(request.POST,instance=address_data)
			try:
				if address_form.is_valid:
					address_form.save()
					return redirect(reverse('user_address'))
				else:
					messages.error(request,"Sorry Address Could'nt Get Updated Try Again ")
					return redirect(reverse('address_detail', kwargs={'id':id}))
			except:
					messages.error(request,"Sorry Address Could'nt Get Updated Try Again ")
					return redirect(reverse('address_detail', kwargs={'id':id})	)
		else:
			return redirect(reverse('login'))

class DeleteAddress(View):
	def get(self,request,id):
		if request.session.get('users_key'):
			address_data = Address.objects.get(user___id = request.session.get('users_key'),_id=id)
			address_data.delete()
			return redirect(reverse('user_address'))
		else:
			return redirect(reverse('login'))

		
class Index(View):
	def get(self,request):
		category_data = Categories.objects.all()
	
		product_Data = Products.objects.all().order_by('Price')[:8]
		if request.session.get('users_key'):
			cart_data = Cart.objects.filter(user___id=request.session.get('users_key')).count()
			request.session['cart_count'] = cart_data
			rendered_data = {
				'categories': category_data,
				'products':product_Data,
				'users':True,
				'cart_count':request.session['cart_count']
			}
		else:
			rendered_data = {
					'categories':category_data,
					'products':product_Data,
				}
		return render(request,'user/index.html',rendered_data)


class AllProducts(View):
	def get(self,request,id):
		rendered_data = {}
		if request.session.get('users_key'):
			rendered_data["users"] = True
			rendered_data["cart_count"] = request.session['cart_count']
		product_data = Products.objects.filter(product_categories=id)
		rendered_data['categories']= Categories.objects.all()
		if product_data:
			page = request.GET.get('page',1)
			paginator = Paginator(product_data,9)
			product_obj = paginator.page(page)
			
			rendered_data["products"] = product_obj
			return render(request,'user/all_products.html',rendered_data)     

		else:
			messages.error(request,'OOps No Product Found.')
			return render(request,'user/all_products.html',rendered_data)       
	   
	def post(self,request,id):
		rendered_data = {}
		rendered_data['categories']= Categories.objects.all()
		if request.session.get('users_key'):
			rendered_data["users"] = True 
			rendered_data["cart_count"] = request.session['cart_count']

		if request.POST.get('search_product'):
			searched_product = request.POST.get('search_product')
			product_data = Products.objects.filter(Q(product_name__contains=searched_product) | Q(  product_enterprsie__enterprise_name__contains=searched_product),product_categories=id)
			if product_data:
				page = request.GET.get('page',1)
				paginator = Paginator(product_data,9)
				product_obj = paginator.page(page)
				rendered_data["products"] = product_obj
				rendered_data["searched_product"] = searched_product
			else:
				messages.error(request,'OOps No Product Found')
				return render(request,'user/all_products.html',rendered_data)	

		elif request.POST.get('filter_by'):
			sort_by = request.POST.get('filter_by')
			if sort_by == 'ascending':
				product_data = Products.objects.filter(product_categories=id).order_by('Price')
			elif sort_by == 'descending':
				product_data = Products.objects.filter(product_categories=id).order_by('-Price')
			else:
				product_data = Products.objects.filter(product_categories=id)
			page = request.GET.get('page',1)
			paginator = Paginator(product_data,9)
			product_obj = paginator.page(page)
			rendered_data["products"] = product_obj
			rendered_data["filtered_product"] = sort_by
		else:
			messages.error(request,'OOps No Product Found')
			return redirect(reverse('all_products', kwargs={'id':id}))
		return render(request,'user/all_products.html',rendered_data)


class ProductDetail(View):
	def get(self,request,id):
		rendered_data = {}
		product_data = Products.objects.get(_id=id)
		products = Products.objects.filter(product_categories=product_data.product_categories).exclude(_id=id)
		category_data = Categories.objects.all()

		if request.session.get('users_key'):
			
			rendered_data = {
				'users':True,
				'cart_count':request.session['cart_count'],
				'product':product_data,
				'products':products,
				'categories':category_data
			}
			return render(request,'user/product_detail.html',rendered_data)
		else:
			rendered_data = {
				'product':product_data,
				'products':products,
				'categories':category_data
			}
			return render(request,'user/product_detail.html',rendered_data)

	

class AddItem(View):
	def get(self,request,id):
		if request.session.get('users_key'):
			cart_data = Cart.objects.filter(user___id=request.session.get('users_key'),product_items___id=id).count()
			if cart_data >0 :
				messages.error(request,'Product Already present in the cart')
				return redirect(reverse('cart'))
		
			else:
				user_data = Users.objects.get(_id = request.session.get('users_key'))
				product = Products.objects.get(_id=id)
				cart_data = Cart(user=user_data,product_items=product)
				cart_data.save()
				request.session['cart_count'] += 1
				messages.success(request,'Product Added to cart')
				return redirect(reverse('cart'))
		else:
			return redirect(reverse('login'))


class RemoveItem(View):
	def get(self,request,id):
		if request.session.get('users_key'):
			cart_data = Cart.objects.get(_id=id)
			cart_data.delete()
			request.session['cart_count'] -= 1
			return redirect(reverse('cart'))
		else:
			return redirect(reverse('login'))


class CartList(View):

	def get(self,request):
		if request.session.get('users_key'):
			cart_data = Cart.objects.filter(user___id=request.session.get('users_key'))	
			sub_total = 0
			item_count = 0

			for item in cart_data:
				item_count += item.qty
				sub_total += item.qty * item.product_items.Price 

			page = request.GET.get('page',1)
			paginator = Paginator(cart_data,5)
			cart_obj = paginator.page(page)
			rendered_data = {
				'cart_item':cart_obj,
				'users':True,
				'sub_total':sub_total,
				'item_count':item_count,
				'cart_count':request.session['cart_count'],
			}
			rendered_data['categories']= Categories.objects.all()
			return render(request,'user/cart.html',rendered_data)
		else:
			return redirect(reverse('login'))

	
	def post(self,request):

		if request.POST.get('selected_qty'):
			product_id = request.POST['product_id']
			product_data = Products.objects.get(_id=product_id)
			qty = request.POST['selected_qty']
			if int(qty) <= product_data.product_qty:
				cart_data = Cart.objects.get(user___id=request.session.get('users_key'),product_items=product_data)
				cart_data.qty = int(qty)
				cart_data.save()
				return redirect(reverse('cart'))
			else:
				messages.error(request,'Sorry that much quantity not available.')
				return redirect(reverse('cart'))

class PlaceOrder(View):

	def get(self,request,slug):

		if request.session.get('users_key'):

			if slug == 'cart':
				address_data = Address.objects.filter(user___id=request.session.get('users_key'))
				address_form = AddressForm()
				cart_data = Cart.objects.filter(user___id=request.session.get('users_key'))
				sub_total = 0
				for item in cart_data:
					sub_total += item.qty * item.product_items.Price 

				rendered_data = {
					'users':True,
					'cart_item':cart_data,
					'address':address_data,
					'addressform':address_form,
					'total':sub_total
				}
				return render(request,'user/checkout.html',rendered_data)

			if request.GET.get('buy_btn'):
				qty = request.GET['selected_qty']
				request.session['selected_qty'] = int(qty)
				product_data = Products.objects.get(_id=slug)

				address_data = Address.objects.filter(user___id=request.session.get('users_key'))
				address_form = AddressForm()
			else:
				product_data = Products.objects.get(_id=slug)

				address_data = Address.objects.filter(user___id=request.session.get('users_key'))
				address_form = AddressForm()

			rendered_data = {
				'users':True,
				'products': product_data,
				'qty' : request.session['selected_qty'],
				'total' : request.session['selected_qty'] * product_data.Price,
				'address': address_data,
				'addressform':address_form,
			}

				
			if not request.session.get('selected_qty'):
				messages.error(request,'You Have Already Palced An Order')
				return redirect(reverse('place_order', kwargs={'slug':slug}))

			if request.session['selected_qty'] <= product_data.product_qty: 
				return render(request,'user/checkout.html',rendered_data)
			
			else:
				messages.error(request,'Sorry that much quantity not available.')
				return redirect(reverse('product_detail', kwargs={'id':slug}))
		
		else:
			return redirect(reverse('login'))

	def post(self,request,slug):
		if request.session.get('users_key'):

			if request.POST.get('add_address'):
				user_data = Users.objects.get(_id = request.session.get('users_key'))
				address_form = AddressForm(request.POST)
				address_form.data._mutable = True
				address_form.data['user'] = user_data
				address_form.data._mutable = False
				if address_form.is_valid:
					address_form.save()	
					messages.success(request,'address was added.')
					return redirect(reverse('place_order', kwargs={'slug':slug}))
				else:
					messages.error(request,'sorry address was not added.')
					return redirect(reverse('place_order', kwargs={'slug':slug}))
		
			user_data = Users.objects.get(_id = request.session.get('users_key'))
			address = request.POST.get('address')
			payment_method = request.POST.get('payment_method')
			order_no = random.randint(111111,999999)

			if slug == 'cart':
					cart_data = Cart.objects.filter(user=user_data)
					total=0
					for item in cart_data:
						total += item.qty * item.product_items.Price
						
						order_obj = Order(order_no=order_no,
										user=user_data,
										product=item.product_items,
										qty=item.qty,
										total=total,
										address=address,
										payment_method=payment_method,
										status='0'
										)
						order_obj.save()
						total=0
						mail_sender_enterprise.delay(order_obj._id)
					cart_data.delete()
					request.session['cart_count'] = 0
				
			elif slug == 'product':
				if request.session.get('selected_qty'):
					product_id = request.POST.get('product')
					qty = request.POST.get('qty')
					product_data = Products.objects.get(_id=product_id)
					total = int(qty) * product_data.Price
					
					order_obj = Order(order_no=order_no,
									user=user_data,
									product=product_data,
									qty=qty,
									total=total,
									address=address,
									payment_method=payment_method,
									status='0'
									)
					order_obj.save()
					mail_sender_enterprise.delay(order_obj._id)
					del request.session['selected_qty']	

					mail_sender_user.delay(order_no,user_data.user_email)		
						
			return render(request,'user/order_success.html',{'users':True})
		else:
			return redirect(reverse('login'))

class OrderHistory(View):
	
	def get(self,request):
		if request.session.get('users_key'):
			
			orders = Order.objects.values('order_no','address','payment_method','ordered_date').annotate(order_count=Count('_id'),total_amount=Sum('total')).filter(user___id=request.session.get('users_key')).order_by('-ordered_date')
			order_list=[]
	
			for order in orders:
				item=list(order.items())
				order_list.append(item)
		
			page = request.GET.get('page',1)
			paginator = Paginator(order_list,6)
			order_obj =  paginator.page(page)

	
			rendered_data = {
				'users':True,
				'orders':order_obj,
				'cart_count': request.session['cart_count']
			}
			rendered_data['categories']= Categories.objects.all()
			return render(request,'user/order_history.html',rendered_data)
		else:
			return redirect(reverse('login'))


class OrderDetail(View):
	def get(self,request,orderno):
		if request.session.get('users_key'):
			order_data = Order.objects.filter(user___id=request.session.get('users_key'),order_no=orderno)

			rendered_data={
				'users': True,
				'cart_count':request.session['cart_count'],
				'orders':order_data
			}	
			rendered_data['categories']= Categories.objects.all()		
			return render(request,'user/order_detail.html',rendered_data)
		else:
			return redirect(reverse('login'))


class OrderHistoryDelete(View):
	
	def get(self,request,orderno):
		if request.session.get('users_key'):

			if orderno == 'all':
				order_data = Order.objects.filter(user___id=request.session.get('users_key'))
				order_data.delete()
				messages.success(request,'Order History Cleared')
				return redirect(reverse('order_history'))
			else:
				order_data = Order.objects.filter(user___id=request.session.get('users_key'),order_no=orderno)
				order_data.delete()
				messages.success(request,'Order History Deleted')
				return redirect(reverse('order_history'))
		else:
			return redirect(reverse('login'))
