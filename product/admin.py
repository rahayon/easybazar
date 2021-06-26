from django.contrib import admin
from .models import Category, Product
from mptt.admin import DraggableMPTTAdmin
from django_summernote.admin import SummernoteModelAdmin


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    #list_display = ['name', 'description', 'is_active'] 
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count

    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count

    related_products_cumulative_count.short_description = 'Related products (in tree)'
    
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'description', 'is_active'] 
#     prepopulated_fields = {'slug': ('name',)}



class ProductAdmin(SummernoteModelAdmin):
    list_display = ['name', 'price', 'discount_price', 'discount','sale_price', 'is_active', 'is_bestseller', 'is_featured', 'created_at']
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['created_at']
    search_fields = ['name','short_description', 'description']
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('description','short_description',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
