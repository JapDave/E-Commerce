from django.urls import path,include
from .views import *


urlpatterns = [
 path('',Enterprise_login.as_view(),name='enterprise_login'),
 path('index/',Enterprise_index.as_view(),name='enterprise_index'),
 path('logout/',Enterprise_logout.as_view(),name='enterprise_logout'),
 path('categories/',Enterprise_category.as_view(),name='enterprise_category')
]
