from .models import Products
import django_filters

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = ['product_name','product_categories']
