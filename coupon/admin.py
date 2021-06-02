from django.contrib import admin
from .models import Coupon
# Register your models here.
@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    '''Admin View for Coupon'''

    list_display = ('code', 'valid_from', 'valid_to', 'discount_percentage','active', )
    list_filter = ('valid_from', 'valid_to', 'active', )
    search_fields = ('code',)
