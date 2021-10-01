from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils.timezone import now
from django.db.models import signals
import uuid


class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)

class Users(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(("UserName"), max_length=50,null=False,blank=False)
    user_password = models.CharField(("Password"), max_length=50,null=False,blank=False)
    user_email = models.EmailField(("E-mail"), max_length=254,blank=False)
    user_photo = models.ImageField(("Profile-photo"), upload_to='User/profile_photo', validators=[FileExtensionValidator(['jpg','jpeg','png'])],height_field=None, width_field=None, max_length=None)
    user_age = models.PositiveIntegerField(("Age"),blank=False)
    user_gender = models.CharField(("Gender"), max_length=50,blank=False)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{10}$")
    user_contact = models.CharField(validators = [phoneNumberRegex], max_length = 10, unique = True)
    user_address1 = models.TextField(("Address"),blank=False)
    user_address2 = models.TextField(("Address2"),blank=True,default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    objects = ParanoidModelManager()


    class Meta:
           verbose_name_plural = "Users"

    def __str__(self):
        return self.user_name

    def delete(self, hard=False, **kwargs):
        if hard:
            super(User, self).delete()
        else:
            self.deleted_at = now()
            self.save()