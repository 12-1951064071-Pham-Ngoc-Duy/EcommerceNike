from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'cart_date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'cart_item_quantity', 'cart_item_is_active')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
