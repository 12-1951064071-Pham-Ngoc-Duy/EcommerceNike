from django.contrib import admin
from .models import Payment, Order, OrderProduct
from django.http import HttpResponse
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from django.utils import timezone

def export_doanh_thu_excel(modeladmin, request, queryset):
    # Tạo workbook mới
    workbook = Workbook()

    # --- Sheet 1: Doanh Thu Hàng Ngày ---
    sheet1 = workbook.active
    sheet1.title = "Doanh Thu Ngày"
    sheet1.append(['Ngày', 'Tổng Doanh Thu'])

    doanh_thu_ngay = Order.objects.annotate(ngay=TruncDay('order_created_at')) \
                                  .values('ngay') \
                                  .annotate(tong_doanh_thu=Sum('order_total'))

    for entry in doanh_thu_ngay:
        # Chuyển đổi ngày thành không có múi giờ
        ngay = entry['ngay'].astimezone(timezone.utc).replace(tzinfo=None)
        sheet1.append([ngay, entry['tong_doanh_thu']])

    # Đặt độ rộng cho cột 'Ngày'
    sheet1.column_dimensions['A'].width = 20  # Có thể điều chỉnh theo ý muốn

    # --- Sheet 2: Doanh Thu Hàng Tháng ---
    sheet2 = workbook.create_sheet(title="Doanh Thu Tháng")
    sheet2.append(['Tháng', 'Tổng Doanh Thu'])

    doanh_thu_thang = Order.objects.annotate(thang=TruncMonth('order_created_at')) \
                                   .values('thang') \
                                   .annotate(tong_doanh_thu=Sum('order_total'))

    for entry in doanh_thu_thang:
        thang = entry['thang'].astimezone(timezone.utc).replace(tzinfo=None)
        sheet2.append([thang, entry['tong_doanh_thu']])

    # Đặt độ rộng cho cột 'Tháng'
    sheet2.column_dimensions['A'].width = 20  # Có thể điều chỉnh theo ý muốn

    # --- Sheet 3: Doanh Thu Hàng Năm ---
    sheet3 = workbook.create_sheet(title="Doanh Thu Năm")
    sheet3.append(['Năm', 'Tổng Doanh Thu'])

    doanh_thu_nam = Order.objects.annotate(nam=TruncYear('order_created_at')) \
                                 .values('nam') \
                                 .annotate(tong_doanh_thu=Sum('order_total'))

    for entry in doanh_thu_nam:
        nam = entry['nam'].astimezone(timezone.utc).replace(tzinfo=None)
        sheet3.append([nam, entry['tong_doanh_thu']])

    # Đặt độ rộng cho cột 'Năm'
    sheet3.column_dimensions['A'].width = 20  # Có thể điều chỉnh theo ý muốn

    # Tạo response trả về file Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="doanh_thu.xlsx"'

    # Lưu workbook vào response
    workbook.save(response)
    return response

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'order_product_quantity', 'order_product_price', 'order_product_ordered')
    extra = 0
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'order_phone', 'order_email', 'order_country', 'order_city', 'order_total', 'order_village', 'order_tax','order_status', 'order_created_at', 'order_is_ordered']
    list_filter = ['order_status', 'order_is_ordered']
    search_fields = ['order_number','payment__payment_id']
    list_per_page = 20
    inlines = [OrderProductInline]
    actions = [export_doanh_thu_excel]
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

admin.site.register(Order,OrderAdmin)