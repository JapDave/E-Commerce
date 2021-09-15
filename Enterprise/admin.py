from django.contrib import admin
from .models import *

class EnterpriseAdmin(admin.AdminSite):
    #admin.site.register(Enterprise_Detail)
    site_header = 'Enterprise Admin'
 

enterprise_admin_site = EnterpriseAdmin(name='enterprise_admin')
enterprise_admin_site.register(Categories)

admin.site.register(Enterprise_Detail)
admin.site.register(Categories)
admin.site.register(Products)