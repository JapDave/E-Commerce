from django.urls import path,include
from .views import *
from Enterprise.admin import enterprise_admin_site

urlpatterns = [
 path('',Enterprise_login.as_view(),name='enterprise_login'),
 path('index/',Enterprise_index.as_view(),name='enterprise_index'),
 path('logout/',Enterprise_logout.as_view(),name='enterprise_logout')
]
