from django import forms
from .models import Users,Order,Address


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ['deleted_at']
        widgets = {'user': forms.HiddenInput(),
                   'postal_address': forms.Textarea(attrs={'rows':4, 'cols':21})
        }
     
class RegisterForm(forms.ModelForm):
    
    class Meta:
        model = Users
        exclude = ['deleted_at',]
        CHOICES = [('M','Male'),('F','Female')]
        widgets = {'user_gender':forms.RadioSelect(choices=CHOICES)}

class ProfileForm(RegisterForm):
    
    class Meta:
        model = Users
        exclude = ['user_password']

       
class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        
        exclude = ['deleted_at']

