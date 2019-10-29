from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=200)
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