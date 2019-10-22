from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=200)

class Products(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    nutriscore = models.CharField(max_length=200)
    fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    barcode = models.IntegerField()
    id_product_json = models.IntegerField()

