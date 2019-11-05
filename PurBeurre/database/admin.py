from django.contrib import admin

from .models import Product, Category, SubstituteCategory, SubstituteProduct

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubstituteCategory)
admin.site.register(SubstituteProduct)