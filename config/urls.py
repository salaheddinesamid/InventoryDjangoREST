"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from stock.views import ProductListView, ProductDetailView, ProductList
from order.views import OrderListView

from user_management.views import AuthenticationView, RegistrationView, ClientListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', ClientListView.as_view()),
    path('stock/', ProductListView.as_view()),
    path('stock/get_all', ProductList.as_view()),
    path('stock/product/', ProductDetailView.as_view()),
    path('orders/', OrderListView.as_view()),
    path('auth/login', AuthenticationView.as_view()),
    path('auth/register', RegistrationView.as_view())
]
