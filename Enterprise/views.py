from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from .models import *
from .forms import ProductForm,EnterpriseForm
# from .filters import ProductFilter


class CategoryFilter(View):
      pass
#     def get(self,request):
#         pass

#     def post(self,request):
#         filtered_categories = {}
#         selected_enterprise = request.POST.get('product_enterprsie')
#         try:
#             if selected_enterprise:
#                 filtered_enterpirse = Enterprise.objects.get(_id=selected_enterprise)
#                 all_categories = filtered_enterpirse.enterprise_categories.all()
#                 filtered_categories = {category.category_name:category._id for category in all_categories}
#         except:
#             pass
#         return JsonResponse(data=filtered_categories, safe=False)


def is_authenticate(request):
    if request.session.get('enterprise_key'):
        
         return True
    return False
        

class Login(View):
    def get(self, request):
        rendered_data = {
            'title':'Enterprise-login',
            'header':'Enterprise'
        }
        return render(request,'login.html',rendered_data)

    def post(self, request):
        user_name = request.POST['username']
        user_password = request.POST['password']
        try:
            fetched_data = Enterprise.objects.filter(enterprise_name=user_name).first()
            if fetched_data != None and fetched_data.enterprise_password == user_password:
                request.session['enterprise_key'] = str(fetched_data._id)
                return redirect(reverse('enterprise_index')) # redirect to Home page
            else:
                raise ValueError() 
        except ValueError:
            messages.error(request,'wrong username or password')
            return redirect(reverse('enterprise_login')) # Wrong credential showed in file
        except Exception as e:
            return HttpResponse('404')# 404 file

class Logout(View):
    def get(self,request):
        if is_authenticate(request):
            del request.session['enterprise_key']
            return redirect(reverse('enterprise_login'))

class Profile(View):
    def get(self,request):
        if is_authenticate(request):
            enterprise_data = Enterprise.objects.filter(_id = request.session.get('enterprise_key')).first()
            form = EnterpriseForm(instance=enterprise_data)
            return render(request,'enterprise/profile.html',{'form':form})
        else:
            return redirect(reverse('enterprise_login'))

    def post(self,request):
        enterprise_data = Enterprise.objects.filter(_id = request.session.get('enterprise_key')).first()
        form=EnterpriseForm(request.POST,request.FILES,instance=enterprise_data) 
        if form.is_valid():
            form.save()
            return render(request,'enterprise/profile.html',{'form':form})
        else:
            print(form.errors)
            return render(request,'enterprise/profile.html',{'form':form})
        

class Index(View):
    def get(self, request):
        try:
            if is_authenticate(request):
                enterprise_data = Enterprise.objects.filter(_id = request.session.get('enterprise_key')).first()
                # categories_data = Categories.objects.all()
                rendered_data = {
                    'enterprise_name':enterprise_data.enterprise_name,
                    # 'categories':categories_data
                }
                return render(request,'enterprise/index.html',rendered_data)
            else:
                return redirect(reverse('enterprise_login'))
        except Exception as e:
            return HttpResponse(e)

           
class ProductsList(View):
    def get(self, request):
        if is_authenticate(request):
            
            products_data  = Products.objects.filter(product_enterprsie = request.session.get('enterprise_key'))
            rendered_data = {
                'products': products_data,
                'total_products':len(products_data)                
            }
            return render(request,'enterprise/list-products.html',rendered_data)
        else:
            return redirect(reverse('enterprise_login'))

    def post(self,request):
        selected_action = request.POST.get( 'actions')
        selected_item = request.POST.getlist('products')
        if selected_item == [] or selected_action == None:
            messages.error(request,'please select item and the prefered action to perform.')
            return redirect(reverse('enterprise_products'))
        else:
            for product in selected_item:
                deleted_product = Products.objects.get(_id=product)
                deleted_product.delete()
            return redirect(reverse('enterprise_products'))
        

class AddProduct(View):
    def get(self,request):
        if is_authenticate(request):
            form=ProductForm()
            enterprise_data = Enterprise.objects.filter(_id = request.session.get('enterprise_key')).first()
            rendered_data = {
                'enterprise':enterprise_data.enterprise_name,
                'form':form
            }
            return render(request,'enterprise/add_product.html',rendered_data)
        else:
            return redirect(reverse('enterprise_login'))

    def post(self,request):
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                    form.save()
                    return redirect(reverse('enterprise_products'))
            else:
                render(request,'enterprise_temp/add_product.html',form=form)
               
class UpdateProduct(View):
    def get(self,request,id):
        if is_authenticate:
            enterprise_data = Enterprise.objects.filter(_id = request.session.get('enterprise_key')).first()
            product_data = Products.objects.get(_id = id)
            form = ProductForm(instance=product_data)
            rendered_data = {
                'enterprise':enterprise_data.enterprise_name,
                'form':form
            }
            return render(request,'enterprise/update_product.html',rendered_data)
        else:
            return redirect(reverse('enterprise_login'))

    
    def post(self,request,id):
            product_data = Products.objects.get(_id = id)
            form = ProductForm(request.POST,request.FILES,instance=product_data)

            if form.is_valid():
                form.save()
                return redirect(reverse('enterprise_products'))
            else:
                render(request,'enterprise/add_product.html',form=form)
         