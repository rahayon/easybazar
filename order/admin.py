from django.contrib import admin
from .models import Order, OrderItem, Refund
# Register your models here.


def make_refund_request_accepted(modeladmin, request, queryset):
    queryset.update(refund_status="Accepted")

make_refund_request_accepted.short_description = 'Update Refund Request Status'
class OrderItemInline(admin.TabularInline):
    '''Admin View for OrderItem'''
    model = OrderItem
    raw_id_fields = ('products',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = ('id','mobile_number','address', 'order_status','get_total_cost','get_total_cost_with_delivery')
    list_filter = ('order_status','refund_status','created_at', 'updated_at',)
    inlines = [OrderItemInline]
    search_fields = ['mobile_number', 'ref_code', 'id']
    ordering = ('-created_at',)
    actions = [make_refund_request_accepted]
admin.site.register(Refund)
   



