"""
URL configuration for mziuri_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>', views.product_detail, name='product_detail'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<int:pk>', views.update_product, name='update_product'),
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add_product_to_cart/<int:id>', views.add_product_to_cart, name='add_product_to_cart'),
    path('remove_cart_item/<int:id>', views.remove_cart_item, name='remove_cart_item'),
    path('confirm_purchase/', views.confirm_purchase, name='confirm_purchase')
]