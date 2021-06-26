from django.urls import path
from .views import PayPaymentView
app_name = 'payment'

urlpatterns = [
    path('pay/<int:pk>/', PayPaymentView.as_view(), name='pay-payment')
]
