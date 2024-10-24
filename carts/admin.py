from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart_item_quantity', 'cart_item_is_active')
    search_fields = (
        'product__product_name',    
    )

admin.site.register(CartItem, CartItemAdmin)
