from django.contrib import admin
from .models import *
# Register your models here.
class ShopAdmin(admin.ModelAdmin):
    admin.site.site_header = 'Shop Admin'
    admin.site.register(User_Detail)
    
