from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from decimal import Decimal
from datetime import date
# Create your models here.


class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='category/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['name']


    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})

    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    
    def latest_product(self):
        d = date.today()
        week = d.isocalendar()[1]
        latest = Category.objects.filter(product__created_at__week=week).distinct()[:9]
        return latest


class Product(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    brand = models.CharField(max_length=50, blank=True)
    sku = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, default=0.00)
    stock = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='product', blank=True, null=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_bestseller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

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
        if self.discount_price and self.discount:
            pass
        elif self.discount_price:
            if self.discount_price>self.price:
                return self.price
            else:
                return self.price-self.discount_price

        elif self.discount:
            return self.price-((self.discount / Decimal(100)) * self.price)
        else:
            return self.price

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    # def discount_product(self):
    #     product = Product.objects.filter(discount=self.discount)
    #     print(product)
    #     return product

    

    # def get_total_discount_item_price(self):
    #     return self.quantity * self.item.discount_price

    # def get_amount_saved(self):
    #     return self.get_total_item_price() - self.get_total_discount_item_price()

    # def get_final_price(self):
    #     if self.item.discount_price:
    #         return self.get_total_discount_item_price()
    #     return self.get_total_item_price()




# def total_income_by_week(self):
#         total = 0
#         d = date.today()
#         week = d.isocalendar()[1]
#         completed_order = Order.order_status.completed().filter(updated_at__week=week)
#         for order in completed_order:
#             total += order.get_total()
#         return total






