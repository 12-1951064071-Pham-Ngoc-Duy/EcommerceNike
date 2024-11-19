from decimal import Decimal
from django.contrib import admin
from suppliers.models import StockEntry
from orders.models import Order
from .models import StatisticsPlaceholder

class StatisticsAdmin(admin.ModelAdmin):
    change_list_template = "admin/statistics_change_list.html"

    def changelist_view(self, request, extra_context=None):
        from django.db.models import Sum

        # Tính toán thống kê
        total_cost = StockEntry.objects.aggregate(total=Sum('total_value'))['total'] or Decimal('0.0')
        total_revenue = Order.objects.filter(order_is_ordered=True).aggregate(total=Sum('order_total'))['total'] or Decimal('0.0')

        # Chuyển đổi kiểu dữ liệu nếu cần
        if isinstance(total_cost, float):
            total_cost = Decimal(str(total_cost))
        if isinstance(total_revenue, float):
            total_revenue = Decimal(str(total_revenue))

        # Tính lợi nhuận
        total_profit = total_revenue - total_cost

        # Thêm dữ liệu thống kê vào context
        extra_context = {
            'total_cost': total_cost,
            'total_revenue': total_revenue,
            'total_profit': total_profit,
        }
        return super().changelist_view(request, extra_context=extra_context)
    def has_add_permission(self, request):
        return False

admin.site.register(StatisticsPlaceholder, StatisticsAdmin)
