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
      list_display = ('product_name', 'product_price', 'product_stock', 'category', 'product_gender', 'product_modifield_date', 'product_is_availabel')
      search_fields = ['product_name']
      readonly_fields = ['product_price','product_stock']
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

class VariationAdmin(admin.ModelAdmin):
      form = VariationForm
      fields = ['product', 'variation_category', 'variation_value', 'variation_is_active','variation_image','stock']
      readonly_fields = ['stock']
      list_display = ('product', 'variation_category', 'variation_value','stock', 'variation_is_active')
      list_editable = ('variation_is_active',)
      list_filter = ('product', 'variation_category', 'variation_value')
      def has_view_permission(self, request, obj=None):
        return request.user.is_staff
      def has_change_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể chỉnh sửa

      def has_add_permission(self, request):
        return request.user.is_staff  # Staff có thể thêm

      def has_delete_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể xóa
      

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
