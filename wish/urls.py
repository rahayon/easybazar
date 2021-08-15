from django.urls import path
from .views import add_to_wishlist, WishListView, remove_from_wish

app_name = 'wish'

urlpatterns =[
    path('', WishListView.as_view(), name='wishes'),
    path('add/<slug:slug>/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<slug:slug>/', remove_from_wish, name='remove_from_wish'),

]