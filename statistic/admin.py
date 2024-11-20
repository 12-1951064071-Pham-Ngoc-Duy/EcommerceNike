from datetime import datetime
from django.db.models import Sum
from decimal import Decimal
from django.contrib import admin
from suppliers.models import StockEntry
from orders.models import Order
from .models import StatisticsPlaceholder
from decimal import Decimal, ROUND_HALF_UP
from django.db.models.functions import TruncMonth, TruncYear

class StatisticsAdmin(admin.ModelAdmin):
    change_list_template = "admin/statistics_change_list.html"

    def changelist_view(self, request, extra_context=None):
        # Hàm làm tròn đến 2 chữ số thập phân
        def round_decimal(value):
            return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # Thống kê theo ngày
        stock_data = (
            StockEntry.objects.values("entry_date__date")
            .annotate(total_cost=Sum("total_value"))
            .order_by("entry_date__date")
        )
        order_data = (
            Order.objects.filter(order_is_ordered=True)
            .values("order_created_at__date")
            .annotate(total_revenue=Sum("order_total"))
            .order_by("order_created_at__date")
        )

        statistics = []
        total_cost_all = Decimal("0.0")
        total_revenue_all = Decimal("0.0")

        dates = set(
            list(stock["entry_date__date"] for stock in stock_data)
            + list(order["order_created_at__date"] for order in order_data)
        )

        for idx, date in enumerate(sorted(dates)):
            stock_entry = next((s for s in stock_data if s["entry_date__date"] == date), None)
            order_entry = next((o for o in order_data if o["order_created_at__date"] == date), None)

            total_cost = Decimal(stock_entry["total_cost"]) if stock_entry else Decimal("0.0")
            total_revenue = Decimal(order_entry["total_revenue"]) if order_entry else Decimal("0.0")
            total_profit = total_revenue - total_cost

            # Làm tròn giá trị
            total_cost = round_decimal(total_cost)
            total_revenue = round_decimal(total_revenue)
            total_profit = round_decimal(total_profit)

            total_cost_all += total_cost
            total_revenue_all += total_revenue

            statistics.append({
                "stt": idx + 1,
                "date": date.strftime("%d-%m-%Y"),
                "total_cost": total_cost,
                "total_revenue": total_revenue,
                "total_profit": total_profit,
            })

        total_profit_all = round_decimal(total_revenue_all - total_cost_all)

        # Thống kê theo tháng
        stock_monthly = (
            StockEntry.objects.annotate(month=TruncMonth("entry_date"))
            .values("month")
            .annotate(total_cost=Sum("total_value"))
            .order_by("month")
        )
        order_monthly = (
            Order.objects.filter(order_is_ordered=True)
            .annotate(month=TruncMonth("order_created_at"))
            .values("month")
            .annotate(total_revenue=Sum("order_total"))
            .order_by("month")
        )

        monthly_statistics = []
        months = set(
            list(stock["month"] for stock in stock_monthly)
            + list(order["month"] for order in order_monthly)
        )

        for idx, month in enumerate(sorted(months)):
            stock_entry = next((s for s in stock_monthly if s["month"] == month), None)
            order_entry = next((o for o in order_monthly if o["month"] == month), None)

            total_cost = Decimal(stock_entry["total_cost"]) if stock_entry else Decimal("0.0")
            total_revenue = Decimal(order_entry["total_revenue"]) if order_entry else Decimal("0.0")
            total_profit = total_revenue - total_cost

            # Làm tròn giá trị
            total_cost = round_decimal(total_cost)
            total_revenue = round_decimal(total_revenue)
            total_profit = round_decimal(total_profit)

            monthly_statistics.append({
                "stt": idx + 1,
                "month": month.strftime("%m-%Y"),
                "total_cost": total_cost,
                "total_revenue": total_revenue,
                "total_profit": total_profit,
            })

        # Thống kê theo năm
        stock_yearly = (
            StockEntry.objects.annotate(year=TruncYear("entry_date"))
            .values("year")
            .annotate(total_cost=Sum("total_value"))
            .order_by("year")
        )
        order_yearly = (
            Order.objects.filter(order_is_ordered=True)
            .annotate(year=TruncYear("order_created_at"))
            .values("year")
            .annotate(total_revenue=Sum("order_total"))
            .order_by("year")
        )

        yearly_statistics = []
        years = set(
            list(stock["year"] for stock in stock_yearly)
            + list(order["year"] for order in order_yearly)
        )

        for idx, year in enumerate(sorted(years)):
            stock_entry = next((s for s in stock_yearly if s["year"] == year), None)
            order_entry = next((o for o in order_yearly if o["year"] == year), None)

            total_cost = Decimal(stock_entry["total_cost"]) if stock_entry else Decimal("0.0")
            total_revenue = Decimal(order_entry["total_revenue"]) if order_entry else Decimal("0.0")
            total_profit = total_revenue - total_cost

            # Làm tròn giá trị
            total_cost = round_decimal(total_cost)
            total_revenue = round_decimal(total_revenue)
            total_profit = round_decimal(total_profit)

            yearly_statistics.append({
                "stt": idx + 1,
                "year": year.year,
                "total_cost": total_cost,
                "total_revenue": total_revenue,
                "total_profit": total_profit,
            })

        # Thêm dữ liệu vào context
        extra_context = extra_context or {}
        extra_context.update({
            "statistics": statistics,
            "monthly_statistics": monthly_statistics,
            "yearly_statistics": yearly_statistics,
            "total_cost": round_decimal(total_cost_all),
            "total_revenue": round_decimal(total_revenue_all),
            "total_profit": round_decimal(total_profit_all),
        })

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False

admin.site.register(StatisticsPlaceholder, StatisticsAdmin)

