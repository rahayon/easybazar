from django.urls import path
from .views import CartDetail, CartAdd, CartRemove

app_name = 'cart'

urlpatterns = [
    path('', CartDetail.as_view(), name='cart-detail'),
    path('add/<int:product_id>/', CartAdd.as_view(), name='cart-add'),
    path('remove/<int:product_id>/', CartRemove.as_view(), name='cart-remove'),
]
