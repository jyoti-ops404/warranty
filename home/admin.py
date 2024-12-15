from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productId', 'productName', 'productImage', 'price')  # Fields to show in the admin list view
    search_fields = ('productId','productName')        # Add search functionality
