# Generated by Django 2.2.6 on 2019-10-29 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0010_auto_20191029_1406'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SubsituteCategory',
            new_name='SubstituteCategory',
        ),
        migrations.RenameModel(
            old_name='SubsituteProduct',
            new_name='SubstituteProduct',
        ),
    ]