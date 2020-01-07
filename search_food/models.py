'''
search_food/models.py
This file contains all models necessary for the search food app.
'''
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    '''
    This model contains all basic products the user searched.
    '''
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    nutriscore = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    barcode = models.BigIntegerField()
    image = models.CharField(max_length=200)
    search = models.CharField(max_length=200)

    def __str__(self):
        '''
        Return the name of the product in backend.
        '''
        return self.name

    class Meta:
        verbose_name_plural = 'products'


class SubstituteProduct(models.Model):
    '''
    This model contains data of the subsitute products.
    '''
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
    in_favorite = models.BooleanField(default=False)

    def __str__(self):
        '''
        Return the name of the subsitute product in backend.
        '''
        return self.name

    class Meta:
        verbose_name_plural = 'Substitute products'


class Favorite(models.Model):
    '''
    This model save the data of products save by the user.
    '''
    product_name = models.CharField(max_length=200)
    barcode = models.BigIntegerField()
    product_associate = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_associate = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=200)

    def __str__(self):
        '''
        Return the name of the favorite in backend.
        '''
        return self.product_name

    class Meta:
        verbose_name_plural = 'Favorites'
