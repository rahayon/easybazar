from django.urls import path
from .views import ProductListView, ProductDetail

app_name = 'product'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('<slug:slug>/', ProductDetail.as_view(), name='Product_detail'),
]
