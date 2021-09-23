from django.contrib import admin
from django import forms
from .models import *


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ['deleted_at']

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        exclude = ['deleted_at']


class EnterpriseForm(forms.ModelForm):
    class Meta:
        model = Enterprise_Detail
        exclude = ['deleted_at']


class CategoriesAdmin(admin.ModelAdmin):
    fields = ('category_name',)
    form = CategoriesForm
    search_fields = ('category_name',)


class EnterpriseAdmin(admin.ModelAdmin):
    form = EnterpriseForm
    search_fields = ('enterprise_name',)

class ProductAdmin(admin.ModelAdmin):
    form = ProductsForm
    search_fields = ('product_name',)
   
    class Media:
        js = ('js/chained_list.js',)


     
admin.site.register(Enterprise_Detail,EnterpriseAdmin)
admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Products,ProductAdmin)
