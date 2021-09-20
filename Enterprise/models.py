from django.db import models
from django.core.validators import RegexValidator
from django.db.models.fields.related import ForeignKey
from djongo import models
from django_paranoid.models import ParanoidModel
#from smart_selects.db_fields import ChainedManyToManyField,ChainedForeignKey



class Categories(ParanoidModel):
    category_name = models.CharField(("Category-Name"), max_length=50,default="")
  
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
    enterprise_categories = models.ArrayReferenceField(Categories, verbose_name=("Enterprise-Categories"),default="")
    
    def __str__(self):
        return self.enterprise_name

class Products(ParanoidModel):
        product_enterprsie = models.ForeignKey(Enterprise_Detail, verbose_name=("Product-Enterprise"), on_delete=models.CASCADE,default="")
        product_categories =models.ForeignKey(Categories, verbose_name=("Product-Categories"), on_delete=models.CASCADE,default="")
        product_name = models.CharField(("Product-Name"), max_length=50,null=False, blank=False)
        product_img = models.ImageField(("Product-image"), upload_to='Product', height_field=None, width_field=None, max_length=None)
        Price = models.PositiveIntegerField(("price"))
        Description = models.TextField(("Description"))
        product_qty = models.PositiveIntegerField(("Product-quantity"))
      
       # product_categories = ChainedForeignKey(,verbose_name=("Product-Categories"),chained_field='product_enterprise',chained_model_field="enterprise_categories",default="")
        
        class Meta:
           verbose_name_plural = "Products"
        
        def __str__(self):
            return self.product_name


