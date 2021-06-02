from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    '''Admin View for OrderItem'''
    model = OrderItem
    raw_id_fields = ('products',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = ('id','full_name','address', 'email', 'postal_code', 'mobile_number')
    list_filter = ('paid','created_at', 'updated_at')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
   