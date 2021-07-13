from django.urls import path
from core.views import FreeShipping, HomeView, ContactUsView
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactUsView.as_view(), name='contact-us'),
    path('free-shipping-charge/',FreeShipping.as_view(), name='free-shipping'),
]
