from django.urls import path,include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
path('',Index.as_view(),name='index'),
path('login/',Login.as_view(),name='login'),
path('logout/',Logout.as_view(),name='logout'),
path('Registeration/',Registeration.as_view(),name='registeration'),
path('forgotpassword/',ForgotPassword.as_view(),name='forgot_password'),
path('otpverification/',OtpVerification.as_view(),name='otp_verification'),
path('changepassword/',ChangePassword.as_view(),name='change_password'),
path('products/<id>',AllProducts.as_view(),name='all_products'),
path('product/<id>',ProductDetail.as_view(),name='product_detail'),
path('addtocart/<id>',AddItem.as_view(),name='add_to_cart'),
path('removecart/<id>',RemoveItem.as_view(),name='remove_from_cart'),
path('cart',CartList.as_view(),name="cart")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

