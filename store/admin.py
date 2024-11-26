from django.contrib import admin

from store.forms import ProductForm, VariationForm
from .models import Product, Variation, ReviewRating,ProductGallery, Supplier
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('image_gallery')
class ProductGalleryInline(admin.TabularInline):
      model = ProductGallery
      extra = 1
      def has_view_permission(self, request, obj=None):
        return request.user.is_staff
      def has_change_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể chỉnh sửa
      def has_delete_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể xóa

class ReviewRatingInline(admin.TabularInline):
      model = ReviewRating
      extra = 0
      def has_view_permission(self, request, obj=None):
        return request.user.is_staff
      def has_view_permission(self, request, obj=None):
        return True
      def has_change_permission(self, request, obj=None):
        return False 
      def has_delete_permission(self, request, obj=None):
        return False
      def has_add_permission(self, request, obj=None):
        return False


class ProductAdmin(admin.ModelAdmin):
      form = ProductForm
      list_display = ('product_name', 'formatted_price', 'product_stock', 'category', 'product_gender', 'product_modifield_date', 'product_is_availabel')
      search_fields = ['product_name']
      readonly_fields = ['product_stock']
      prepopulated_fields = {'product_slug': ('product_name',)}
      inlines = [ProductGalleryInline, ReviewRatingInline]
      def has_view_permission(self, request, obj=None):
        return request.user.is_staff
      def has_change_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể chỉnh sửa

      def has_add_permission(self, request):
        return request.user.is_staff  # Staff có thể thêm

      def has_delete_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể xóa
      def formatted_price(self, obj):
        return "{:,.0f}".format(obj.product_price)  # Định dạng với dấu phẩy
      formatted_price.short_description = 'Giá'

class VariationAdmin(admin.ModelAdmin):
      form = VariationForm
      fields = ['product', 'variation_category','variation_color', 'variation_value','variation_size', 'variation_is_active','stock']
      readonly_fields = []
      list_display = ('product', 'variation_color', 'variation_size','stock', 'variation_is_active')
      list_editable = ('variation_is_active',)
      list_filter = ('product',)
      def has_view_permission(self, request, obj=None):
        return request.user.is_staff
      def has_change_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể chỉnh sửa

      def has_add_permission(self, request):
        return request.user.is_staff  # Staff có thể thêm

      def has_delete_permission(self, request, obj=None):
        return request.user.is_staff
      

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
