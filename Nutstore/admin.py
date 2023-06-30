from django.contrib import admin
from .models import Product, Warehouse, CartItem, City,  Order

admin.site.register(Product)
admin.site.register(Warehouse)
admin.site.register(CartItem)
admin.site.register(City)
admin.site.register(Order)
