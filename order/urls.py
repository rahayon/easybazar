from django.urls import path
from .views import CancelOrder, OrderCreateView, OrderHistory, RefundRequest

app_name = 'order'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('order_history/', OrderHistory.as_view(), name="order-history"),
    path('refund_request/', RefundRequest.as_view(), name='refund-request'),
    path('cacel/<int:pk>/', CancelOrder.as_view(), name='cancel-order')
]
