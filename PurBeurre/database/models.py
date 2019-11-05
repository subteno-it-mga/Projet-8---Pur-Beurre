from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=200)
    category_test = models.CharField(max_length=200)
    fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    barcode = models.BigIntegerField()
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'products'

class Category(models.Model):

    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class SubstituteProduct(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    nutriscore = models.IntegerField()
    fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    barcode = models.BigIntegerField()
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Substitute products'


class SubstituteCategory(models.Model):

    name = models.CharField(max_length=200)
    product_subsitute = models.ForeignKey(SubstituteProduct, on_delete=models.CASCADE)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Substitute categories'

class Favorite(models.Model):

    product_name = models.CharField(max_length=200)
    user_associated = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Favorites'