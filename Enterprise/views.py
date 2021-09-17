from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from .models import *


def is_authenticate(request):
    if request.session.get('enterprise_key'):
        return True
    return False
        


class Enterprise_login(View):
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

class Enterprise_logout(View):
    def get(self,request):
        if is_authenticate(request):
            del request.session['enterprise_key']
            return redirect(reverse('enterprise_login'))

class Enterprise_index(View):
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

           

class Enterprise_category(View):
    def get(self, request):
        if is_authenticate(request):
            enterprise_data = Enterprise_Detail.objects.filter(id = request.session.get('enterprise_key')).first()
            rendered_data = {
                'categories':enterprise_data.enterprise_categories.all()
            }
            return render(request,'enterprise_temp/list-categories.html',rendered_data)
        else:
            return redirect(reverse('enterprise_login'))

