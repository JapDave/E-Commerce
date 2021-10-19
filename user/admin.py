from django.contrib import admin
from .models import Users,Order,Address
from .forms import OrderForm, RegisterForm
from django.utils.html import format_html


class AddressAdmin(admin.StackedInline):
    model = Address
    exclude= ['deleted_at']

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra


class UserAdmin(admin.ModelAdmin):
    admin.site.site_header = 'Shop Admin'
    form = RegisterForm
    inlines = [AddressAdmin,]


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_per_page = 10
    list_display = ('get_user','get_image','get_enterprise','get_product_name','qty','status','created_at')
    ordering = ('-created_at',)


    @admin.display(description='User Name')
    def get_user(self,obj):
        return obj.user.user_name

    @admin.display(description='Product Image')
    def get_image(self,obj):
        return format_html('<img src="{}" width=70px height=65px/>'.format(obj.product.product_img.url))

    @admin.display(description='Enterprise Name')
    def get_enterprise(self,obj):
        return obj.product.product_enterprsie.enterprise_name

    @admin.display(description='Product Name')
    def get_product_name(self,obj):
        return obj.product.product_name




admin.site.register(Users,UserAdmin)
admin.site.register(Order,OrderAdmin)
    
