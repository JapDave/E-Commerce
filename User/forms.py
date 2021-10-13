from django import forms
from .models import Users,Order,Address


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ['deleted_at']
        widgets = {'user': forms.HiddenInput()}

class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = Users
        exclude = ['deleted_at',]
        CHOICES = [('M','Male'),('F','Female')]
        widgets = {'user_gender':forms.RadioSelect(choices=CHOICES)}
        


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ['deleted_at']

