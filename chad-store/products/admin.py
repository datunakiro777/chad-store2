from django.contrib import admin
from products.models import Product, ProductTag, Review

admin.site.register(Product)
admin.site.register(ProductTag)
admin.site.register(Review)
