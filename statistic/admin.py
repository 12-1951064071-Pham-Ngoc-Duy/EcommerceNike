from django.db.models import Sum
from django.contrib import admin
from suppliers.models import StockEntry
from orders.models import Order
from .models import StatisticsChartPlaceholder, StatisticsPlaceholder
from django.db.models.functions import TruncMonth, TruncYear
import json

class StatisticsAdmin(admin.ModelAdmin):
    change_list_template = "admin/statistics_change_list.html"

    def changelist_view(self, request, extra_context=None):
        # Hàm làm tròn đến 2 chữ số thập phân

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
        total_cost_all = 0
        total_revenue_all = 0
        previous_day_revenue = None  # Doanh thu ngày hôm trước

        dates = set(
            list(stock["entry_date__date"] for stock in stock_data)
            + list(order["order_created_at__date"] for order in order_data)
        )

        for idx, date in enumerate(sorted(dates)):
            stock_entry = next((s for s in stock_data if s["entry_date__date"] == date), None)
            order_entry = next((o for o in order_data if o["order_created_at__date"] == date), None)

            total_cost = stock_entry["total_cost"] if stock_entry else 0
            total_revenue = order_entry["total_revenue"] if order_entry else 0
            total_profit = total_revenue - total_cost

            total_cost_all += total_cost
            total_revenue_all += total_revenue

            # Tính % tăng trưởng theo ngày
            growth_rate = None
            if previous_day_revenue is not None and previous_day_revenue > 0:
                growth_rate = ((total_revenue - previous_day_revenue) / previous_day_revenue) * 100
                growth_rate = growth_rate
            else:
                growth_rate = 0  # Trường hợp không có doanh thu ngày hôm trước

            statistics.append({
                "stt": idx + 1,
                "date": date.strftime("%d-%m-%Y"),
                "total_cost": format(total_cost, ","),
                "total_revenue": format(total_revenue, ","),
                "total_profit": format(total_profit, ","),
                "growth_rate": f"{growth_rate:.2f}%",
            })

            previous_day_revenue = total_revenue  # Cập nhật doanh thu ngày hôm trước

        total_profit_all = total_revenue_all - total_cost_all

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
        previous_month_revenue = None  # Doanh thu tháng trước

        for idx, month in enumerate(sorted(months)):
            stock_entry = next((s for s in stock_monthly if s["month"] == month), None)
            order_entry = next((o for o in order_monthly if o["month"] == month), None)

            total_cost = stock_entry["total_cost"] if stock_entry else 0
            total_revenue = order_entry["total_revenue"] if order_entry else 0
            total_profit = total_revenue - total_cost

            # Tính % tăng trưởng theo tháng
            growth_rate = None
            if previous_month_revenue is not None and previous_month_revenue > 0:
                growth_rate = ((total_revenue - previous_month_revenue) / previous_month_revenue) * 100
                growth_rate = growth_rate
            else:
                growth_rate = 0

            monthly_statistics.append({
                "stt": idx + 1,
                "month": month.strftime("%m-%Y"),
                "total_cost": format(total_cost, ","),
                "total_revenue": format(total_revenue, ","),
                "total_profit": format(total_profit, ","),
                "growth_rate": f"{growth_rate:.2f}%",
            })

            previous_month_revenue = total_revenue

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
        previous_year_revenue = None  # Doanh thu năm trước

        for idx, year in enumerate(sorted(years)):
            stock_entry = next((s for s in stock_yearly if s["year"] == year), None)
            order_entry = next((o for o in order_yearly if o["year"] == year), None)

            total_cost = stock_entry["total_cost"] if stock_entry else 0
            total_revenue = order_entry["total_revenue"] if order_entry else 0
            total_profit = total_revenue - total_cost

            # Tính % tăng trưởng theo năm
            growth_rate = None
            if previous_year_revenue is not None and previous_year_revenue > 0:
                growth_rate = ((total_revenue - previous_year_revenue) / previous_year_revenue) * 100
                growth_rate = growth_rate
            else:
                growth_rate = 0

            yearly_statistics.append({
                "stt": idx + 1,
                "year": year.year,
                "total_cost": format(total_cost, ","),
                "total_revenue": format(total_revenue, ","),
                "total_profit": format(total_profit, ","),
                "growth_rate": f"{growth_rate:.2f}%",
            })

            previous_year_revenue = total_revenue

        # Thêm dữ liệu vào context
        extra_context = extra_context or {}
        extra_context.update({
            "statistics": statistics,
            "monthly_statistics": monthly_statistics,
            "yearly_statistics": yearly_statistics,
            "total_cost": format(total_cost_all, ","),
            "total_revenue": format(total_revenue_all, ","),
            "total_profit":format(total_profit_all, ","),
            "daily_chart_data": json.dumps([
                {
                "date": stat["date"],
                "total_cost": float(stat["total_cost"].replace(",", "")),
                "total_revenue": float(stat["total_revenue"].replace(",", "")),
                "total_profit": float(stat["total_profit"].replace(",", ""))
                } 
                for stat in statistics
            ]),
            "monthly_chart_data": json.dumps([
                {
                "month": stat["month"],
                "total_cost": float(stat["total_cost"].replace(",", "")),
                "total_revenue": float(stat["total_revenue"].replace(",", "")),
                "total_profit": float(stat["total_profit"].replace(",", ""))
                } 
                for stat in monthly_statistics
            ]),
            "yearly_chart_data": json.dumps([
                {
                "year": stat["year"],
                "total_cost": float(stat["total_cost"].replace(",", "")),
                "total_revenue": float(stat["total_revenue"].replace(",", "")),
                "total_profit": float(stat["total_profit"].replace(",", ""))
                } 
                for stat in yearly_statistics
            ]),
        })

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False



class ChartStatisticsAdmin(admin.ModelAdmin):
    change_list_template = "admin/chart_statistics_change_list.html"

    def changelist_view(self, request, extra_context=None):
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
        total_cost_all = 0
        total_revenue_all = 0
        previous_day_revenue = None  # Doanh thu ngày hôm trước

        dates = set(
            list(stock["entry_date__date"] for stock in stock_data)
            + list(order["order_created_at__date"] for order in order_data)
        )

        for idx, date in enumerate(sorted(dates)):
            stock_entry = next((s for s in stock_data if s["entry_date__date"] == date), None)
            order_entry = next((o for o in order_data if o["order_created_at__date"] == date), None)

            total_cost = stock_entry["total_cost"] if stock_entry else 0
            total_revenue = order_entry["total_revenue"] if order_entry else 0
            total_profit = total_revenue - total_cost

            total_cost_all += total_cost
            total_revenue_all += total_revenue

            # Tính % tăng trưởng theo ngày
            growth_rate = None
            if previous_day_revenue is not None and previous_day_revenue > 0:
                growth_rate = ((total_revenue - previous_day_revenue) / previous_day_revenue) * 100
            else:
                growth_rate = 0  # Trường hợp không có doanh thu ngày hôm trước

            statistics.append({
                "stt": idx + 1,
                "date": date.strftime("%d-%m-%Y"),
                "total_cost": format(total_cost, ","), 
                "total_revenue": format(total_revenue, ","), 
                "total_profit": format(total_profit, ","), 
                "growth_rate": f"{growth_rate:.2f}%",
            })

            previous_day_revenue = total_revenue  # Cập nhật doanh thu ngày hôm trước

        total_profit_all = total_revenue_all - total_cost_all

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
        previous_month_revenue = None  # Doanh thu tháng trước

        for idx, month in enumerate(sorted(months)):
            stock_entry = next((s for s in stock_monthly if s["month"] == month), None)
            order_entry = next((o for o in order_monthly if o["month"] == month), None)

            total_cost = stock_entry["total_cost"] if stock_entry else 0
            total_revenue = order_entry["total_revenue"] if order_entry else 0
            total_profit = total_revenue - total_cost

            # Tính % tăng trưởng theo tháng
            growth_rate = None
            if previous_month_revenue is not None and previous_month_revenue > 0:
                growth_rate = ((total_revenue - previous_month_revenue) / previous_month_revenue) * 100
            else:
                growth_rate = 0

            monthly_statistics.append({
                "stt": idx + 1,
                "month": month.strftime("%m-%Y"),
                "total_cost": format(total_cost, ","), 
                "total_revenue": format(total_revenue, ","), 
                "total_profit": format(total_profit, ","), 
                "growth_rate": f"{growth_rate:.2f}%",
            })

            previous_month_revenue = total_revenue

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
        previous_year_revenue = None  # Doanh thu năm trước

        for idx, year in enumerate(sorted(years)):
            stock_entry = next((s for s in stock_yearly if s["year"] == year), None)
            order_entry = next((o for o in order_yearly if o["year"] == year), None)

            total_cost = stock_entry["total_cost"] if stock_entry else 0
            total_revenue = order_entry["total_revenue"] if order_entry else 0
            total_profit = total_revenue - total_cost

            # Tính % tăng trưởng theo năm
            growth_rate = None
            if previous_year_revenue is not None and previous_year_revenue > 0:
                growth_rate = ((total_revenue - previous_year_revenue) / previous_year_revenue) * 100
            else:
                growth_rate = 0

            yearly_statistics.append({
                "stt": idx + 1,
                "year": year.year,
                "total_cost": format(total_cost, ","), 
                "total_revenue": format(total_revenue, ","), 
                "total_profit": format(total_profit, ","), 
                "growth_rate": f"{growth_rate:.2f}%",
            })

            previous_year_revenue = total_revenue

        # Thêm dữ liệu vào context
        extra_context = extra_context or {}
        extra_context.update({
            "statistics": statistics,
            "monthly_statistics": monthly_statistics,
            "yearly_statistics": yearly_statistics,
            "total_cost": format(total_cost_all, ","), 
            "total_revenue": format(total_revenue_all, ","), 
            "total_profit": format(total_profit_all, ","), 
            "daily_chart_data": json.dumps([{
                "date": stat["date"],
                "total_cost": float(stat["total_cost"].replace(",", "")),
                "total_revenue": float(stat["total_revenue"].replace(",", "")),
                "total_profit": float(stat["total_profit"].replace(",", ""))
            } for stat in statistics]),
            "monthly_chart_data": json.dumps([{
                "month": stat["month"],
                "total_cost": float(stat["total_cost"].replace(",", "")),
                "total_revenue": float(stat["total_revenue"].replace(",", "")),
                "total_profit": float(stat["total_profit"].replace(",", ""))
            } for stat in monthly_statistics]),
            "yearly_chart_data": json.dumps([{
                "year": stat["year"],
                "total_cost": float(stat["total_cost"].replace(",", "")),
                "total_revenue": float(stat["total_revenue"].replace(",", "")),
                "total_profit": float(stat["total_profit"].replace(",", ""))
            } for stat in yearly_statistics]),
        })

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False

admin.site.register(StatisticsPlaceholder, StatisticsAdmin)
admin.site.register(StatisticsChartPlaceholder, ChartStatisticsAdmin)