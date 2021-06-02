from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Coupon(models.Model):

    code = models.CharField(max_length=50,unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount_percentage = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], blank=True)
    active = models.BooleanField()


    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("Coupon_detail", kwargs={"pk": self.pk})