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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"

    def __str__(self):
        return self.website_name

    def get_absolute_url(self):
        return reverse("Setting_detail", kwargs={"pk": self.pk})

class ContactUs(models.Model):

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "ContactUs"
        verbose_name_plural = "ContactUs"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ContactUs_detail", kwargs={"pk": self.pk})





class Banner(models.Model):

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    banner_tag = models.CharField(max_length=30)
    bannager_image = models.ImageField(upload_to="banner/")
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Banner_detail", kwargs={"pk": self.pk})

    @property
    def image_url(self):
        try:
            url = self.bannager_image.url
        except:
            url = ''
        return url
