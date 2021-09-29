from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _


class ProductForm(forms.ModelForm):
   
    class Meta:
        model = Products
        exclude = ['product_enterprsie','deleted_at']
       

class EnterpriseForm(forms.ModelForm):

    class Meta:
        model = Enterprise
        exclude = ['deleted_at']
        labels = {
            'enterprise_name':_('Enterprise-Name'),
            'enterprise_password':_('Password'),
            'enterprise_email':_('Email-id'),
            'enterprise_photo':_('Profile-Photo'),
            'enterprise_contact':_('Contact-No')
        }
    