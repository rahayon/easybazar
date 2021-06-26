from django.contrib import admin
from .models import DeliveryLocation, DeliveryType
# Register your models here.
@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    '''Admin View for DeliveryLocation'''

    list_display = ('location_name', 'delivery_target_amount')
    list_filter = ('location_name',)   

@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    '''Admin View for Delivery'''

    list_display = ('location','type_of_delivery', 'delivery_charge',)
    list_filter = ('location','type_of_delivery',)
    #inlines = [DeliveryLocationInline,]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)


