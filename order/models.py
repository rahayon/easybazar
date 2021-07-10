from django.db import models
from django.urls import reverse
from product.models import Product
from coupon.models import Coupon
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from delivery.models import DeliveryType
from django.conf import settings
# Create your models here.



class Order(models.Model):
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=254)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_coupon')
    coupon_discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    delivery = models.ForeignKey(DeliveryType, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_delivery')
    delivery_charge = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    is_ordered = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f' Order {self.id}'

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.coupon_discount/Decimal(100))
    
    def get_total_cost_with_delivery(self):
        return self.get_total_cost() + self.delivery_charge

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("OrderItem_detail", kwargs={"pk": self.pk})

    def get_cost(self):
        return self.price * self.quantity



    




