from django.contrib import admin
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

      def has_add_permission(self, request, obj=None):
        # Kiểm tra quyền: chỉ cho phép thêm nếu obj đã tồn tại (tức là sản phẩm đã được tạo)
        if obj is None:
            return False  # Không cho phép thêm nếu sản phẩm chưa tồn tại
        return super().has_add_permission(request, obj)

      def has_delete_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể xóa

class ReviewRatingInline(admin.TabularInline):
      model = ReviewRating
      extra = 0
      def has_view_permission(self, request, obj=None):
        return request.user.is_staff


class ProductAdmin(admin.ModelAdmin):
      list_display = ('product_name', 'product_price', 'product_stock', 'category', 'product_gender', 'product_modifield_date', 'product_is_availabel')
      search_fields = ['product_name']
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
      list_display = ('product', 'variation_category', 'variation_value', 'variation_is_active')
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
