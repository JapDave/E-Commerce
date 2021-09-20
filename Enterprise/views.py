from django import http
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from .models import *
# from .filters import ProductFilter


class CategoryFilter(View):
    def get(self,request):
        pass

    def post(self,request):
        filtered_categories = {}
        selected_enterprise = request.POST.get('product_enterprsie')
        print(selected_enterprise)
        try:
            if selected_enterprise:
                filtered_enterpirse = Enterprise_Detail.objects.get(id=selected_enterprise)
                all_categories = filtered_enterpirse.enterprise_categories.all()
                # for cat in all_categories:
                #     print(cat.id)
                filtered_categories = {category.category_name:category.id for category in all_categories}
       
        except:
            pass
     
        return JsonResponse(data=filtered_categories, safe=False)


def is_authenticate(request):
    if request.session.get('enterprise_key'):
        return True
    return False
        


class EnterpriseLogin(View):
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
            fetched_data = Enterprise_Detail.objects.filter(enterprise_name=user_name).first()
            if fetched_data != None and fetched_data.enterprise_password == user_password:
                request.session['enterprise_key'] = fetched_data.id
                return redirect(reverse('enterprise_index')) # redirect to Home page
            else:
                raise ValueError() 
        except ValueError:
            messages.error(request,'wrong username or password')
            return redirect(reverse('enterprise_login')) # Wrong credential showed in file
        except Exception as e:
            return HttpResponse('404')# 404 file

class EnterpriseLogout(View):
    def get(self,request):
        if is_authenticate(request):
            del request.session['enterprise_key']
            return redirect(reverse('enterprise_login'))

class EnterpriseIndex(View):
    def get(self, request):
        try:
            if is_authenticate(request):
                enterprise_data = Enterprise_Detail.objects.filter(id = request.session.get('enterprise_key')).first()
                categories_data = Categories.objects.all()
                rendered_data = {
                    'enterprise_name':enterprise_data.enterprise_name,
                    'categories':categories_data
                }
                return render(request,'enterprise_temp/index.html',rendered_data)
            else:
                return redirect(reverse('enterprise_login'))

        except Exception as e:
            return HttpResponse('404')

           

class EnterpriseProducts(View):
    def get(self, request):
        if is_authenticate(request):
            products_data  = Products.objects.filter(product_enterprsie_id = request.session.get('enterprise_key'))
            rendered_data = {
                'products': products_data,
                'total_products':len(products_data)
            }
            return render(request,'enterprise_temp/list-products.html',rendered_data)
        else:
            return redirect(reverse('enterprise_login'))

    def post(self,request):
            if request.POST.get('search_text') != None:
                searched_text = request.POST.get('search_text')
                filtered_product = Products.objects.filter(product_name__contains = searched_text,product_enterprsie_id = request.session.get('enterprise_key'))
                rendered_data = {
                    'filtered_products':filtered_product,
                    'searched_text':searched_text,
                    'total_products':len(filtered_product)
                }
                return render(request,'enterprise_temp/list-products.html',rendered_data)
            elif request.POST['submit_action']:
                selected_action = request.POST.get( 'actions')
                selected_item = request.POST.getlist('products')
                if selected_item == None or selected_action == None:
                    messages.error(request,'please select item and the prefered action to perform.')
                    return redirect(reverse('enterprise_products'))
                else:
                    for product_id in selected_item:
                        deleted_product = Products.objects.get(id=product_id)
                        deleted_product.delete()
                    return redirect(reverse('enterprise_products'))
          

class EnterpriseProductAdd(View):
    def get(self,request):
        if is_authenticate(request):
            enterprise_data = Enterprise_Detail.objects.filter(id = request.session.get('enterprise_key')).first()
            rendered_data = {
                'enterprise':enterprise_data
            }
            return render(request,'enterprise_temp/add_product.html',rendered_data)
       
        else:
            return redirect(reverse('enterprise_login'))

    def post(self,request):
        pass