# Generated by Django 2.2.6 on 2019-11-05 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0015_remove_favorite_barcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='category',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='product_name',
        ),
    ]
