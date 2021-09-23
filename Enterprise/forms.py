from django import forms
from .models import *

class ProductForm(forms.ModelForm):
   
    class Meta:
        model = Products
        exclude = ['product_enterprsie','product_categories','deleted_at']