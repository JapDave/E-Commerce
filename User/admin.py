from django.contrib import admin
from .models import *
from .forms import RegisterForm


class UserAdmin(admin.ModelAdmin):
    admin.site.site_header = 'Shop Admin'
    form = RegisterForm

class CartAdmin(admin.ModelAdmin):
    exclude = ['deleted_at']
    list_display = ('user','get_product_item')


    @admin.display(description='Product-Items', ordering='product_items__product_name')
    def get_product_item(self,obj):
        product_data = obj.product_items.all()
        product_item = {product.product_name for product in product_data}
        print(product_item)
        return product_item


admin.site.register(Cart,CartAdmin)
admin.site.register(Users,UserAdmin)

    
