from django.db import models
from django.core.validators import RegexValidator
from djongo import models

class Categories(models.Model):
    category_name = models.CharField(("Category-Name"), max_length=50)

    class Meta:
           verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class Enterprise_Detail(models.Model):
    enterprise_name = models.CharField(("Enterprise-Name"), max_length=50, null=False, blank=False)
    enterprise_password = models.CharField(("Password"), max_length=50, null=False, blank=False)
    enterprise_email = models.EmailField(("E-mail"),null=False, blank=False)
    enterprise_photo = models.ImageField(("Profile-photo"), upload_to='Enterprise/profile_photo', height_field=None, width_field=None, max_length=None)
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    enterprise_contact = models.CharField(validators = [phoneNumberRegex], max_length = 13, unique = True)
    enterprise_categories = models.ArrayReferenceField(to=Categories,on_delete=models.CASCADE,default="")

    def __str__(self):
        return self.enterprise_name

class Products(models.Model):
        product_name = models.CharField(("Product-Name"), max_length=50,null=False, blank=False)
        product_img = models.ImageField(("Product-image"), upload_to='Product', height_field=None, width_field=None, max_length=None)
        Price = models.PositiveIntegerField(("price"))
        Description = models.TextField(("Description"))
        product_qty = models.PositiveIntegerField(("Product-quantity"))
        product_category = models.ForeignKey(Categories, verbose_name=("Product-Category"), on_delete=models.CASCADE)
        product_enterprise = models.ForeignKey(Enterprise_Detail, verbose_name=("Product-Enterprise"), on_delete=models.CASCADE)
        
        class Meta:
           verbose_name_plural = "Products"

        def __str__(self):
            return self.product_name