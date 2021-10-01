from django.contrib import admin
from .models import *
from .forms import RegisterForm


class UserAdmin(admin.ModelAdmin):
    admin.site.site_header = 'Shop Admin'
    form = RegisterForm


admin.site.register(Users,UserAdmin)
    
