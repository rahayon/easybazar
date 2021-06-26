from delivery.views import DeliveryApply
from django.urls import path

app_name = 'delivery'

urlpatterns = [
    path('apply/', DeliveryApply.as_view(),  name='delivery-apply')
]
