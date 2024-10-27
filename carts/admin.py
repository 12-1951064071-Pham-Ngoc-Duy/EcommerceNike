from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart_item_quantity', 'cart_item_is_active')
    search_fields = (
        'product__product_name',    
    )
    def has_delete_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False 

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'cart_date_added')
    def delete_model(self, request, obj):
        CartItem.objects.filter(cart=obj).delete()
        super().delete_model(request, obj)
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_view_or_change_permission(self, request, obj=None):
        return True
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart,CartAdmin)
