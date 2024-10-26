from django.contrib import admin
from .models import Category
from .forms import CategoryForm
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    prepopulated_fields = {'category_slug': ('category_name',)}
    list_display = ('category_name', 'category_slug')
    search_fields = (
        'category_name',    
    )
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể chỉnh sửa

    def has_add_permission(self, request):
        return request.user.is_staff  # Staff có thể thêm

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff  # Staff có thể xóa
admin.site.register(Category, CategoryAdmin)