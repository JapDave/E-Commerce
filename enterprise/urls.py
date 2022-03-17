from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

 path('',Login.as_view(),name='enterprise_login'),
 path('index/',Index.as_view(),name='enterprise_index'),
 path('logout/',Logout.as_view(),name='enterprise_logout'),
 path('forgotpassword/',ForgotPassword.as_view(),name='forgot_password'),
 path('otpverification/',OtpVerification.as_view(),name='otp_verification'),
 path('changepassword/',ChangePassword.as_view(),name='change_password'),
 path('profile/',Profile.as_view(),name='enterprise_profile'),
 path('userchangepassword/',ProfileChangePassword.as_view(),name='profile_enterprise_change_password'),
 path('products/',ProductsList.as_view(),name='product_list'),
 path('add/',AddProduct.as_view(),name='product_add'),
 path('delete/<id>',DeleteProduct.as_view(),name='product_delete'),
 path('change/<id>',UpdateProduct.as_view(),name='product_update'),
 path('orders',OrderRequest.as_view(),name='order_requests'),
 path('orderdetail/<id>',OrderDetail.as_view(),name='order_detail'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
