from django.contrib import admin
from .models import Product
from .models import Vendor, Warranty

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productId', 'productName', 'productImage', 'price')  # Fields to show in the admin list view
    search_fields = ('productId','productName')        # Add search functionality



@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # Show ID and name in the admin list view

@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'full_name', 'email', 'phone', 'model', 'date_of_sale', 'serial_number']