from django.urls import path
from .views import CartDetail, CartAdd, CartRemove
app_name = 'cart'

urlpatterns = [
    path('', CartDetail.as_view(), name='cart-detail'),
    path('add/<int:product_id>/', CartAdd.as_view(), name='cart-add'),
    path('remove/<int:product_id>/', CartRemove.as_view(), name='cart-remove'),
    # path('wish/<int:product_id>/', WishListAdd.as_view(), name='wish-add'),
    # path('wish/remove/<int:product_id>/', WishListRemove.as_view(), name='wish-remove'),
    # path('wishlist/', WishDetail.as_view(), name='wish-detail'),
    # path('wish/add/<int:product_id>/', WishToCartAdd.as_view(), name='wish-to-cart-add'),
]
