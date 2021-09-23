from django.db import models
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils.timezone import now
from djongo import models
import uuid

class ParanoidModelManager(models.Manager):
    def get_queryset(self):
        return super(ParanoidModelManager, self).get_queryset().filter(deleted_at__isnull=True)


class ParanoidModel(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True,null=True ,default=None)
    objects = ParanoidModelManager()

    class Meta:
        abstract = True

    def delete(self, hard=False, **kwargs):
        if hard:
            super(ParanoidModel, self).delete()
        else:
            self.deleted_at = now()
            self.save()

class Categories(ParanoidModel):
    category_name = models.CharField(("Category-Name"),max_length=50)
   
    class Meta:
           verbose_name_plural = "Categories"
          
    def __str__(self):
        return self.category_name


class Enterprise_Detail(ParanoidModel):
    enterprise_name = models.CharField(("Enterprise-Name"), max_length=50, null=False, blank=False)
    enterprise_password = models.CharField(("Password"), max_length=50, null=False, blank=False)
    enterprise_email = models.EmailField(("E-mail"),null=False, blank=False)
    enterprise_photo = models.ImageField(("Profile-photo"), upload_to='Enterprise/profile_photo', height_field=None, width_field=None, max_length=None)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    enterprise_contact = models.CharField(validators = [phoneNumberRegex], max_length = 13, unique = True)
    enterprise_categories = models.ArrayReferenceField(to=Categories, db_column='enterprise_categories',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)
 
    class Meta:
           verbose_name_plural = "Enterprises"

    def __str__(self):
        return self.enterprise_name

class Products(ParanoidModel):
    product_enterprsie = models.ForeignKey(Enterprise_Detail, db_column='product_enterprise', verbose_name=("Product-Enterprise"), on_delete=models.CASCADE)
    product_categories = models.ForeignKey(Categories, db_column='product_categories', verbose_name=("Product-Categories"), on_delete=models.CASCADE)
    product_name = models.CharField(("Product-Name"), max_length=50, null=False, blank=False)
    product_img = models.ImageField(("Product-image"), upload_to='Product', height_field=None, width_field=None,validators=[FileExtensionValidator(['jpg','jpeg','png'])] ,max_length=None)
    Price = models.PositiveIntegerField(("price"))
    Description = models.TextField(("Description"))
    product_qty = models.PositiveIntegerField(("Product-quantity"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.product_name


