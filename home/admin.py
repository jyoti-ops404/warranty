from django.contrib import admin
from .models import Product, ProductType, Vendor, Warranty,ContactUs,Inquiry

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productId', 'productName', 'productImage', 'price')  # Fields to show in the admin list view
    list_filter = ['type', 'featured']
    search_fields = ('productId','productName')        # Add search functionality

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']  # Show ID and name in the admin list view
    search_fields = ('id','name')

@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'full_name', 'email', 'phone', 'model', 'date_of_sale', 'serial_number']
    list_filter = ('vendor',)
    search_fields = ('vendor__name', 'full_name', 'serial_number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Allow superuser to see all data
        if hasattr(request.user, 'vendor'):  # Check if the user is a vendor
            return qs.filter(vendor__name=request.user.get_full_name())
        return qs.none()  # Non-superusers without a vendor should see no data

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'phone', 'email')