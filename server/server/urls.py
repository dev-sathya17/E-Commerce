"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from amazon.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signUp/", Register.as_view()),
    path('login/', Login.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('category/', Category.as_view()),
    path('category/<str:category_id>/', CategoryInfo.as_view()),
    path('spec/', Specification.as_view()),
    path('spec/<str:spec_id>/', SpecInfo.as_view()),
    path('address/', Address.as_view()),
    path('address/<str:address_id>/', AddressInfo.as_view()),
    path('userAddress/<str:user_id>/', GetUserAddresses.as_view()),
    path('userDefaultAddress/<str:user_id>/', GetUserDefaultAddress.as_view()),
    path('cards/', Card.as_view()),
    path('cards/<str:card_id>/', CardInfo.as_view()),
    path('userCards/<str:user_id>/', GetUserCards.as_view()),
    path('validCard/',validate_card),
    path('products/', Product.as_view()),
    path('products/<str:product_id>/', ProductInfo.as_view()),
    path('cart/', Cart.as_view()),
    path('cart/<str:cart_id>/', CartOperations.as_view()),
    path('userCart/<str:user_id>/', CartInfo.as_view()),
    path('wishlist/', Wishlist.as_view()),
    path('userList/<str:user_id>/', WishlistInfo.as_view()),
    path('wishlistProduct/<str:product_id>/', WishlistOperations.as_view()),
]
