from django.db import models
from django.core.validators import RegexValidator
from datetime import date
#To Create a custom user user model and admin panel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy

#To create automatically one to one object. It will create user with userprofile automatically
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
# Create your models here.


class MyUserManager(BaseUserManager):
    def _create_user(self, mobile, password, **extra_fields):
        """Create and saves a user with a given email and password"""

        if not mobile:
            raise ValueError("The mobile number must be set!")

        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(mobile, password, **extra_fields)


phone_regex = RegexValidator(
    regex=r'^01[13-9]\d{8}$', message="Phone number must be entered in the format: '01300000000'. Up to 11 digits allowed.")
class CustomerQuerySet(models.QuerySet):
    def all_customer(self):
        return self.filter(is_staff=False, is_superuser=False)
    def customer_by_month(self):
        month = date.today().month
        
        return self.filter(is_staff=False, is_superuser=False, created_at__month=month)
class CustomerManager(models.Manager):
    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def all_customer(self):
        return self.get_queryset().all_customer()
        
    def customer_by_month(self):
        return self.get_queryset().customer_by_month()
        
class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(unique=True, null=False, max_length=11, validators=[phone_regex])
    email = models.EmailField(max_length=254, blank=True)
    device = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(
        ugettext_lazy('staff status'),
        default=False,
        help_text=ugettext_lazy(
            'Designates whether the user can log in this site')
    )
    is_active = models.BooleanField(
        ugettext_lazy('active'),
        default=True,
        help_text=ugettext_lazy(
            'Designate whether this user should be treated as active. unselect this instead of deleting accounts')
    )
    USERNAME_FIELD = 'mobile'
    objects = MyUserManager()
    customers = CustomerManager()

    def __str__(self):
        return self.mobile

    def get_full_name(self):
        return self.mobile

    def get_short_name(self):
        return self.mobile

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=254, blank=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True)
    address = models.CharField(max_length=254, blank=True)
    def __str__(self):
        return self.user.email + "'s Profile"


    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]
        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True
    

    def get_absolute_url(self):
        return reverse("UserProfile_detail", kwargs={"pk": self.pk})

        
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
