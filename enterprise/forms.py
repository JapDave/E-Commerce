from django import forms
from .models import *


class ProductForm(forms.ModelForm):
   
    class Meta:
        model = Products
        exclude = ['deleted_at']
        widgets = {'product_enterprsie': forms.HiddenInput(),
                   'Description': forms.Textarea(attrs={'rows':4, 'cols':22})
        }
        
class EnterpriseForm(forms.ModelForm):

    class Meta:
        model = Enterprise
        exclude = ['enterprise_password','deleted_at']

    
      