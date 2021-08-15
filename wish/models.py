from django.db import models
from django.conf import settings
from product.models import Product


# Create your models here.
class WishList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_wishlist')
    product = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.profile.full_name

    # def get_absolute_url(self):
    #     return reverse("product", kwargs={"slug": self.slug})
