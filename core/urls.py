from django.urls import path
from core.views import FreeShipping, HomeView, ContactUsView, PrivacyPolicy, RefundPolicy, TermsCoditions
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactUsView.as_view(), name='contact-us'),
    path('free-shipping-charge/',FreeShipping.as_view(), name='free-shipping'),
    path('pryvacy_policy/', PrivacyPolicy.as_view(), name='privacy-policy'),
    path('refund_policy/', RefundPolicy.as_view(), name='refund-policy'),
    path('terms_conditions/', TermsCoditions.as_view(), name='terms-conditions'),
]
