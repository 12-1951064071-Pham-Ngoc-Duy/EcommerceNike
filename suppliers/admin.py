from django.contrib import admin
import openpyxl
from django.http import HttpResponse

from suppliers.forms import StockEntryForm, SupplierForm
from .models import Supplier, StockEntry
from django.db.models import Sum
from django.utils.timezone import now
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
# Register your models here.
def export_daily_monthly_yearly_costs_to_excel(modeladmin, request, queryset):
    # Lấy năm hiện tại để đặt tên file
    current_year = now().year

    # Nhóm dữ liệu theo ngày, tháng và năm rồi tính tổng chi tiêu
    daily_data = (
        queryset
        .annotate(day=ExtractDay('entry_date'))
        .values('day')
        .annotate(total_cost=Sum('total_value'))
    )
    monthly_data = (
        queryset
        .annotate(month=ExtractMonth('entry_date'))
        .values('month')
        .annotate(total_cost=Sum('total_value'))
    )
    yearly_data = (
        queryset
        .annotate(year=ExtractYear('entry_date'))
        .values('year')
        .annotate(total_cost=Sum('total_value'))
    )

    # Tạo workbook mới
    workbook = openpyxl.Workbook()

    # Tạo sheet cho từng trường (ngày, tháng, năm)
    day_sheet = workbook.active  # Sheet mặc định là cho ngày
    day_sheet.title = 'Daily Costs'
    month_sheet = workbook.create_sheet(title='Monthly Costs')
    year_sheet = workbook.create_sheet(title='Yearly Costs')

    # Thêm tiêu đề cho các cột
    day_sheet.append(['Day', 'Total Cost'])
    month_sheet.append(['Month', 'Total Cost'])
    year_sheet.append(['Year', 'Total Cost'])

    # Thêm dữ liệu vào sheet cho Ngày
    total_daily_cost = 0  # Biến để giữ tổng chi phí trong ngày
    for entry in daily_data:
        total_daily_cost += entry['total_cost']
        day_sheet.append([entry['day'], float(entry['total_cost'])])

    # Thêm dữ liệu vào sheet cho Tháng
    total_monthly_cost = 0  # Biến để giữ tổng chi phí trong tháng
    for entry in monthly_data:
        total_monthly_cost += entry['total_cost']
        month_sheet.append([entry['month'], float(entry['total_cost'])])

    # Thêm dữ liệu vào sheet cho Năm
    total_yearly_cost = 0  # Biến để giữ tổng chi phí trong năm
    for entry in yearly_data:
        total_yearly_cost += entry['total_cost']
        year_sheet.append([entry['year'], float(entry['total_cost'])])

    # Thêm hàng tổng cộng vào mỗi sheet
    day_sheet.append(['Total', total_daily_cost])
    month_sheet.append(['Total', total_monthly_cost])
    year_sheet.append(['Total', total_yearly_cost])

    # Thiết lập response để trả về file Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=costs_{current_year}.xlsx'
    workbook.save(response)
    return response
export_daily_monthly_yearly_costs_to_excel.short_description = "Xuất Chi Phí Ra Excel"
class SupplierAdmin(admin.ModelAdmin):
    form = SupplierForm
    list_display = ['supplier_name', 'supplier_email', 'supplier_phone', 'supplier_country', 'supplier_is_active']
    search_fields = ['supplier_name', 'supplier_email']
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        form.save_m2m()
class StockEntryAdmin(admin.ModelAdmin):
    form = StockEntryForm
    fields = ['product', 'supplier', 'quantity','total_value', 'unit_price','stock_category','stock_color','stock_value','stock_size']
    list_display = ['product', 'supplier', 'quantity','total_value', 'unit_price']  # Hiển thị thông tin trong danh sách
    readonly_fields = ['total_value']
    search_fields = ['supplier__supplier_name']
    actions = [export_daily_monthly_yearly_costs_to_excel]  # Thêm action vào admin
    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(StockEntry, StockEntryAdmin)
admin.site.register(Supplier, SupplierAdmin)