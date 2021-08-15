from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from decimal import Decimal
from datetime import date
from taggit.managers import TaggableManager
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count


# Create your models here.


class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            blank=True, null=True, related_name='children')
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
        latest = Category.objects.filter(
            product__created_at__month=month).distinct()[:9]
        return latest

    def children_category(self):
        return self.get_children()

    def discount_with_category(self):
        # return self.product.discount_product()
        product = [p for p in Product.objects.filter(category=self) if p.discount_price or p.discount]
        return product

    def product_by_category(self):
        category = self.get_children()
        if category:
            products = []
            for category in self.get_family():
                for p in category.product.all():
                    products.append(p)
            return products
        else:
            products = Product.objects.filter(category=self)
            return products


class Color(models.Model):
    color_name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.color_name

    def get_absolute_url(self):
        return reverse("Color_detail", kwargs={"pk": self.pk})


class Size(models.Model):
    size_name = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self):
        return self.size_name

    def get_absolute_url(self):
        return reverse("Size_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    UNIT_STATUS = (
        ('gm', 'gm'),
        ('Kg', 'Kg'),
        ('ml', 'ml'),
        ('Litre', 'Litre')
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
    unit = models.FloatField(default=0.0)
    unit_status = models.CharField(
        max_length=20, choices=UNIT_STATUS, default='Kg')
    on_sale = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product/')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='product', blank=True, null=True)
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    color = models.ManyToManyField(Color, related_name='product_color', blank=True)
    size = models.ManyToManyField(Size, related_name='product_size', blank=True)
    video = models.URLField(max_length=200, blank=True)
    is_bestseller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
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
            if self.discount_price > self.price:
                return self.price
            else:
                return self.price - self.discount_price

        elif self.discount:
            return self.price - ((self.discount / Decimal(100)) * self.price)
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
        product = [p for p in Product.objects.all(
        ) if p.discount_price or p.discount]
        return product

    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def get_average_rating_product(self):
        ratings = ReviewRating.objects.annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:6]
        return ratings


class ReviewRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_rating')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    subject = models.CharField(max_length=50)
    review = models.TextField(max_length=500)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ReviewRating"
        verbose_name_plural = "ReviewRatings"

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse("ReviewRating_detail", kwargs={"pk": self.pk})



