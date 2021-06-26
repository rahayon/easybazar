from django.db import models
from django.urls import reverse
# Create your models here.
class DeliveryLocation(models.Model):
    location_name = models.CharField(max_length=100)
    delivery_target_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = "Delivery Location"
        verbose_name_plural = "Delivery Locations"

    def __str__(self):
        return self.location_name

    def get_absolute_url(self):
        return reverse("DeliveryLocation_detail", kwargs={"pk": self.pk})


class DeliveryType(models.Model):
    """
    ডেলিভারী লোকেশন অনুযায়ী টাকার পরিমান পরিবর্তিত হবে। যদি অর্ডারের পরিমান নির্দিষ্ট হয় যেমন ১০০০০টাকা হয় তাহলে ডেলিভারী চার্জ ফ্রি হবে।
    """
    DELIVERY_TYPE = (
        ('Free','Free'),
        ('Flat', 'Flat')
    )
    location = models.ForeignKey(DeliveryLocation, on_delete=models.SET_NULL, related_name='deliverable_location', blank=True, null=True)
    type_of_delivery = models.CharField(max_length=50, choices=DELIVERY_TYPE, default='Flat')
    delivery_charge = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Type of Delivery"
        verbose_name_plural = "Type of  Deliveries"

    def __str__(self):
        return self.location.location_name+" "+self.type_of_delivery+" "+"Tk."+str(self.delivery_charge)

    def get_absolute_url(self):
        return reverse("DeliveryType_detail", kwargs={"pk": self.pk})

