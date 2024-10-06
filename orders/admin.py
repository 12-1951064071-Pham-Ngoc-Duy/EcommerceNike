from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'order_product_quantity', 'order_product_price', 'order_product_ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'order_phone', 'order_email', 'order_country', 'order_city', 'order_total', 'order_village', 'order_tax','order_status', 'order_created_at', 'order_is_ordered']
    list_filter = ['order_status', 'order_is_ordered']
    search_fields = ['order_number', 'order_first_name', 'order_last_name', 'order_phone', 'order_email']
    list_per_page = 20
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)


