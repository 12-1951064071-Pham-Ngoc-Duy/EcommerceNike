from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart_item_quantity', 'cart_item_is_active')
    search_fields = (
        'product__product_name',    
    )
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False 
admin.site.register(CartItem, CartItemAdmin)
