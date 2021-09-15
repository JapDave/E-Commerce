from django.core import mail
from django.db import models
from django.db.models.fields import EmailField, PositiveIntegerField
from django.core.validators import RegexValidator

class User_Detail(models.Model):
    user_name = models.CharField(("UserName"), max_length=50,null=False,blank=False)
    user_password = models.CharField(("Password"), max_length=50,null=False,blank=False)
    user_email = models.EmailField(("E-mail"), max_length=254,blank=False)
    user_photo = models.ImageField(("Photo"), upload_to='user_upload/profile_photo', height_field=None, width_field=None, max_length=None)
    user_age = models.PositiveIntegerField(("Age"),blank=False)
    user_gender = models.CharField(("Gender"), max_length=50,blank=False)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    user_contact = models.CharField(validators = [phoneNumberRegex], max_length = 13, unique = True)
    user_address = models.TextField(("Address"),blank=False)

    def __str__(self):
        return self.user_name
