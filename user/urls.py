from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
#User Basic Start
path('',Index.as_view(),name='index'),
path('faqs',Faqs.as_view(),name='faqs'),
path('aboutus',Aboutus.as_view(),name='aboutus'),
path('login/',Login.as_view(),name='login'),
path('logout/',Logout.as_view(),name='logout'),
path('registeration/',Registeration.as_view(),name='registeration'),
path('forgotpassword/',ForgotPassword.as_view(),name='user_forgot_password'),
path('otpverification/',OtpVerification.as_view(),name='user_otp_verification'),
path('changepassword/',ChangePassword.as_view(),name='user_change_password'),
path('profile/',Profile.as_view(),name='user_profile'),
path('userchangepassword/',ProfileChangePassword.as_view(),name='profile_user_change_password'),
path('address/',UserAddress.as_view(),name='user_address'),
path('addressdetail/<id>',AddressDetail.as_view(),name='address_detail'),
path('deleteaddress/<id>',DeleteAddress.as_view(),name='delete_address'),
path('products/<id>',AllProducts.as_view(),name='all_products'),
path('product/<id>',ProductDetail.as_view(),name='product_detail'),
path('placeorder/<slug>',PlaceOrder.as_view(),name='place_order'),
path('orderhistory',OrderHistory.as_view(),name='order_history'),
path('orderdelete/<orderno>',OrderHistoryDelete.as_view(),name='order_history_delete'),
path('orderdetail/<orderno>',OrderDetail.as_view(),name='user_order_detail'),
path('addtocart/<id>',AddItem.as_view(),name='add_to_cart'),
path('removecart/<id>',RemoveItem.as_view(),name='remove_from_cart'),
path('cart',CartList.as_view(),name="cart")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

