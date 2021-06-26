from order.models import Order
from django.db import models
from django.urls import reverse


class PaymentType(models.Model):
    MERCHANT_TYPE = (
        ('Agent','Agent'),
        ('Personal','Personal')
    )
    payment_name = models.CharField(max_length=100)
    merchant_number = models.CharField(max_length=30,blank=True)
    merchant_status = models.CharField(max_length=50,choices=MERCHANT_TYPE, default='Agent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PaymentType"
        verbose_name_plural = "PaymentTypes"

    def __str__(self):
        return self.payment_name

    def get_absolute_url(self):
        return reverse("PaymentType_detail", kwargs={"pk": self.pk})


class Payment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='payment_order')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, related_name='payment', blank=True, null=True)
    mobile_number = models.CharField(max_length=30,blank=True)
    transaction_id = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return self.order.mobile_number

    def get_absolute_url(self):
        return reverse("Payment_detail", kwargs={"pk": self.pk})
