from django.urls import path
from .views import CouponApply

app_name = 'coupon'

urlpatterns = [
    path('apply/', CouponApply.as_view(), name='coupon-apply')
]
