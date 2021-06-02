from django.contrib import admin
from django.contrib.admin.decorators import register
from django.db import models
from .models import Category, Product
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active'] 
    prepopulated_fields = {'slug': ('name',)}



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'old_price', 'is_active', 'is_bestseller', 'is_featured', 'created_at']
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['created_at']
    search_fields = ['name','short_description', 'description']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
