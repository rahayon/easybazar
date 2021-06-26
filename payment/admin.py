from payment.models import PaymentType
from django.contrib import admin
from .models import PaymentType, Payment
# Register your models here.
admin.site.register(PaymentType)
admin.site.register(Payment)