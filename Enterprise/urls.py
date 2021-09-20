from django.urls import path,include
from .views import *


urlpatterns = [
 path('',EnterpriseLogin.as_view(),name='enterprise_login'),
 path('index/',EnterpriseIndex.as_view(),name='enterprise_index'),
 path('logout/',EnterpriseLogout.as_view(),name='enterprise_logout'),
 path('products/',EnterpriseProducts.as_view(),name='enterprise_products'),
 path('add/',EnterpriseProductAdd.as_view(),name='product_add'),

]
