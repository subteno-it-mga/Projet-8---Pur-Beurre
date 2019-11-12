from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    nutriscore = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    barcode = models.BigIntegerField()
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'products'

class SubstituteProduct(models.Model):

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    nutriscore = models.IntegerField()
    fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    barcode = models.BigIntegerField()
    image = models.CharField(max_length=200)
    original = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Substitute products'

class Favorite(models.Model):

    product_name = models.CharField(max_length=200)
    barcode = models.BigIntegerField()
    product_associate = models.ForeignKey(SubstituteProduct, on_delete=models.CASCADE)
    user_associate = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name_plural = 'Favorites'