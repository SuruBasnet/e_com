from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name='home' ),
    path('product-page/<str:pk>/' , views.product_page , name='product' ),
    path('productform/' , views.createproduct , name='productform' ),
    path('editproduct/<str:pk>/' , views.editproduct , name='editproduct' ),
    path('deleteproduct/<str:pk>/' , views.deleteproduct , name='deleteproduct' ),
    path('addcart/<str:pk>/' , views.Addcart , name='addcart' ),
    path('deletecart/<str:pk>/' , views.deleteitem , name='deleteitem' ),
    path('cart/' , views.Cartitem , name='cart' ),
    path('checkout/<str:pk>/' , views.checkout , name='checkout' ),
    path('login-page/' , views.loginpage , name='login' ),
    path('register-page/' , views.registerpage , name='register' ),
    path('logout-page/' , views.logoutpage , name='logout' ),
]