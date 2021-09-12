from django.urls import path
from core.views import AboutUs, FreeShipping, HomeView, ContactUsView, OurService, PrivacyPolicy, RefundPolicy, TermsCoditions
app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactUsView.as_view(), name='contact-us'),
    path('about/',AboutUs.as_view(), name='about-us'),
    path('free-shipping-charge/',FreeShipping.as_view(), name='free-shipping'),
    path('pryvacy_policy/', PrivacyPolicy.as_view(), name='privacy-policy'),
    path('refund_policy/', RefundPolicy.as_view(), name='refund-policy'),
    path('terms_conditions/', TermsCoditions.as_view(), name='terms-conditions'),
    path('our_services/', OurService.as_view(), name='our-service'),
]
