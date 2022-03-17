from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils.timezone import now
from django.db.models import signals
from djongo import models
import uuid

class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)


class Categories(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(("Category-Name"),max_length=50)
    category_image = models.ImageField(("Category-Image"), upload_to='Category', height_field=None, width_field=None, max_length=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
    objects = ParanoidModelManager()
   
    class Meta:
           verbose_name_plural = "Categories"
          
    def __str__(self):
        return self.category_name
   
    def delete(self, hard=False, **kwargs):
        cls = self.__class__
        signals.pre_delete.send(sender=cls, instance=self)

        if hard:
            super(Categories, self).delete()
        else:
            self.deleted_at = now()
            self.save()
 

class Enterprise(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enterprise_name = models.CharField(("Enterprise-Name"), max_length=50, null=False, blank=False)
    enterprise_password = models.CharField(("Password"), max_length=64, null=False, blank=False)
    enterprise_email = models.EmailField(("E-mail"),null=False, blank=False,unique=True)
    enterprise_photo = models.ImageField(("Profile-photo"), upload_to='Enterprise/profile_photo', height_field=None, width_field=None, max_length=None)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{10}$")
    enterprise_contact = models.CharField(validators = [phoneNumberRegex],max_length = 10, unique = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    objects = ParanoidModelManager()
    

    class Meta:
           verbose_name_plural = "Enterprises"

    def __str__(self):
        return self.enterprise_name

    def delete(self, hard=False, **kwargs):
        cls = self.__class__
        signals.pre_delete.send(sender=cls, instance=self)
        
        if hard:
            super(Enterprise, self).delete()
        else:
            self.deleted_at = now()
            self.save()
   
   
class Products(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_enterprsie = models.ForeignKey(Enterprise,on_delete=models.CASCADE,null=True,blank=True,verbose_name=("Product-Enterprise") )
    product_categories = models.ForeignKey(Categories,on_delete=models.CASCADE, verbose_name=("Product-Categories"))
    product_name = models.CharField(("Product-Name"), max_length=50, null=False, blank=False)
    product_img = models.ImageField(("Product-image"), upload_to='Product', height_field=None, width_field=None,validators=[FileExtensionValidator(['jpg','jpeg','png','webp'])] ,max_length=None)
    Price = models.PositiveIntegerField(("price"))
    Description = models.TextField(("Description"))
    product_qty = models.PositiveIntegerField(("Product-quantity"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
    objects = ParanoidModelManager()

    class Meta:
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.product_name

    def delete(self, hard=False, **kwargs):
        if hard:
            super(Products, self).delete()
        else:
            self.deleted_at = now()
            self.save()