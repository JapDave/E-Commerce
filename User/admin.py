from django.contrib import admin
from .models import *
from .forms import OrderForm, RegisterForm


class UserAdmin(admin.ModelAdmin):
    admin.site.site_header = 'Shop Admin'
    form = RegisterForm

class OrderAdmin(admin.ModelAdmin):
    form = OrderForm




admin.site.register(Users,UserAdmin)
admin.site.register(Order,OrderAdmin)
    
