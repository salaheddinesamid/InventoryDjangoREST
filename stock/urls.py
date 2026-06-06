from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='stock'),
    path('product/', views.ProductDetailView.as_view(), name='stock_details'),
]
