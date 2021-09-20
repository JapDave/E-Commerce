from django.contrib import admin
from django import forms
from .models import *
from django_paranoid.admin import ParanoidAdmin

class ProductsForm(forms.ModelForm):
    class Meta:
        model : Products

class CategoriesAdmin(ParanoidAdmin,admin.ModelAdmin):
    #  list_filter = ('category_name',)
     search_fields = ('category_name',)

class EnterpriseAdmin(ParanoidAdmin,admin.ModelAdmin):
    #  list_filter = ('enterprise_name',)
     search_fields = ('enterprise_name',)

class ProductAdmin(ParanoidAdmin,admin.ModelAdmin):
    #  list_filter = ('product_name',)
      search_fields = ('product_name',)
      form = ProductsForm
     
      class Media:
            js = ('js/chained_list.js',)


     
admin.site.register(Enterprise_Detail,EnterpriseAdmin)
admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Products,ProductAdmin)
