'''
search_food/apps.py
File to manage admin space.
'''
from django.contrib import admin

from .models import Product, SubstituteProduct, Favorite, PBLanguage

admin.site.register(Product)
admin.site.register(SubstituteProduct)
admin.site.register(Favorite)
admin.site.register(PBLanguage)
