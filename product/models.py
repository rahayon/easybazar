from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from decimal import Decimal
from datetime import date
from taggit.managers import TaggableManager
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


    # def __str__(self):
    #     full_path = [self.name]
    #     k = self.parent
    #     while k is not None:
    #         full_path.append(k.name)
    #         k = k.parent

    #     return ' -> '.join(full_path[::-1])
    def __str__(self):
        return self.name

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
        today = date.today()
        month = today.month
        latest = Category.objects.filter(product__created_at__month=month).distinct()[:9]
        return latest






class Product(models.Model):
    UNIT_STATUS = (
        ('gm','gm'),
        ('Kg','Kg'),
        ('ml','ml'),
        ('L','L')
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    brand = models.CharField(max_length=50, blank=True)
    sku = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, default=0.00)
    discount = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    unit = models.IntegerField(default=0)
    unit_status = models.CharField(max_length=20, choices=UNIT_STATUS, default='Kg')
    image = models.ImageField(upload_to='product/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='product', blank=True, null=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    tags = TaggableManager()
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
        
        if self.discount_price:
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
    
    @property
    def check_avialable(self):
        if self.stock > 0:
            return True
        return False

    def discount_product(self):
        product = [p for p in Product.objects.all() if p.discount_price or p.discount]
        return product







