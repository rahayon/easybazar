from django.db import models
from django.urls import reverse
# Create your models here.


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Product(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    brand = models.CharField(max_length=50, blank=True)
    sku = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    old_price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, default=0.00)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product/')
    category = models.ManyToManyField(Category)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_bestseller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:Product_detail", kwargs={"slug": self.slug})

    @property
    def sale_price(self):
        if self.old_price>self.price:
            return self.price
        else:
            return None
    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    # def get_total_discount_item_price(self):
    #     return self.quantity * self.item.discount_price

    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_discount_item_price()

    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.get_total_discount_item_price()
    #     return self.get_total_item_price()








