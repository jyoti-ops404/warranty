from django.db import models
from django.contrib.auth.models import User

from django.db import models

class ProductType(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to='product_type_images/')

    def __str__(self):
        return self.name

class Product(models.Model):
    productId = models.TextField()
    productName = models.TextField()
    productImage = models.ImageField(upload_to='product_images/')
    price = models.FloatField()
    Ah = models.IntegerField(null=True, blank=True)
    Volt = models.IntegerField(null=True, blank=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    highlights = models.TextField(null=True, blank=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.productId

class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Vendor linked to a user

    def __str__(self):
        return self.name

class Warranty(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='warranties')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    model = models.CharField(max_length=255)
    date_of_sale = models.DateField()
    serial_number = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.full_name} - {self.model}"
    
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Inquiry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inquiries")
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Inquiry by {self.name} for {self.product.productName}"