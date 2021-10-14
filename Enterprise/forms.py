from django import forms
from .models import *



class ProductForm(forms.ModelForm):
   
    class Meta:
        model = Products
        exclude = ['deleted_at']
        widgets = {'product_enterprsie': forms.HiddenInput()}
       
        
       
class EnterpriseForm(forms.ModelForm):

    class Meta:
        model = Enterprise
        exclude = ['enterprise_password','deleted_at']

    
      