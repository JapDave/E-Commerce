from django.contrib import admin
from django import forms
from .models import *
from django.contrib.auth.apps import AuthConfig
from django.utils.html import format_html


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
        model = Enterprise
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
    list_per_page = 10
    list_display = ('product_name','get_product_name','get_category_name','created_at','Price','get_image')

    @admin.display(description='Enterprise Name', ordering='product_enterprsie__enterprise_name')
    def get_product_name(self, obj):
        return obj.product_enterprsie.enterprise_name
    
    @admin.display(description='Category Name', ordering='product_categories__enterprise_categories')
    def get_category_name(self, obj):
        return obj.product_categories.category_name

    @admin.display(description='Image')
    def get_image(self, obj):
        return format_html('<img src="{}" width=80px height=75px/>'.format(obj.product_img.url))




    # class Media:
    #     js = ('js/chained_list.js',)


     
admin.site.register(Enterprise,EnterpriseAdmin)
admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Products,ProductAdmin)
