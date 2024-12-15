from django.db import models

class Product(models.Model):
    productId = models.TextField()
    productName = models.TextField()
    productImage = models.ImageField()
    price = models.FloatField()

    def __str__(self):
        return self.productId
