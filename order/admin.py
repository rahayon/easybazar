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

    list_display = ('id','mobile_number','address', 'is_ordered','get_total_cost','get_total_cost_with_delivery')
    list_filter = ('is_ordered','created_at', 'updated_at')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
   



