from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html
from django.contrib.auth.models import Group
from .forms import AdminAccountsForm, UserProfileAdminForm
# Register your models here.
class AccountAdmin(UserAdmin):
    form = AdminAccountsForm
    list_display = (
        'email', 'first_name', 'last_name', 'username', 
        'phone_number', 'date_of_birth', 'place',
        'country', 'city', 'village', 'last_login', 
        'date_joined', 'is_active', 'is_admin', 'is_staff', 'is_superadmin'
    )
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        ('Thông tin cá nhân', {
                    'fields': ('first_name', 'last_name', 'email', 'phone_number', 'username', 'date_of_birth')
                }),
        ('Địa chỉ', {
                    'fields': ('country', 'city', 'village', 'place')
                }),
        ('Trạng thái tài khoản', {
            'fields': ('is_active','is_admin', 'is_staff', 'is_superadmin')
                }),
    )
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff  # Cho phép staff xem model này

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.user_profile_picture and object.user_profile_picture.url:
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.user_profile_picture.url))
        else:
            return format_html('<span style="color: gray;">Không có ảnh</span>')

    thumbnail.short_description = 'Ảnh hồ sơ'

    form = UserProfileAdminForm
    list_display = (
        'thumbnail', 'user', 'user_profile_country', 
        'user_profile_city', 'user_profile_village', 
        'user_profile_address', 'user_profile_date_of_birth'
    )
    search_fields = ('user__email',)

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff  # Cho phép staff xem model này

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(Group)
