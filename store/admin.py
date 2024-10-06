from django.contrib import admin
from .models import Product, Variation, ReviewRating
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
      list_display = ('product_name', 'product_price', 'product_stock', 'category', 'product_gender', 'product_modifield_date', 'product_is_availabel')
      prepopulated_fields = {'product_slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
      list_display = ('product', 'variation_category', 'variation_value', 'variation_is_active')
      list_editable = ('variation_is_active',)
      list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)