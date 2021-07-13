from django.db import models
from django.urls import reverse

# Create your models here.
class Setting(models.Model):
    website_name = models.CharField(max_length=150)
    address = models.CharField(max_length=254, blank=True)
    mobile1 = models.CharField(max_length=50, blank=True)
    mobile2 = models.CharField(max_length=50, blank=True)
    email =  models.EmailField( max_length=254, blank=True)
    facebook = models.URLField(max_length=200, blank=True)
    twitter = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    instagram = models.URLField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Setting_detail", kwargs={"pk": self.pk})




