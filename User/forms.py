from django import forms
from django.forms import widgets
from .models import Users,Order

class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ("__all__")
        exclude = ['deleted_at']
        CHOICES = [('M','Male'),('F','Female')]
        widgets = {'user_gender':forms.RadioSelect(choices=CHOICES)}

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ['deleted_at']