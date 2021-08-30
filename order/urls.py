from django.urls import path
from .views import OrderCreateView, order_history

app_name = 'order'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('order_history/', order_history, name="order-history"),
]
