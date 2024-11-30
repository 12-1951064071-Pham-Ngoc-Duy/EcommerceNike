from django.db import models

# Create your models here.
class StatisticsPlaceholder(models.Model):
    class Meta:
        verbose_name = "Thống kê"
        verbose_name_plural = "Thống kê"

class StatisticsChartPlaceholder(models.Model):
    class Meta:
        verbose_name = "Biểu đồ thống kê"
        verbose_name_plural = "Biểu đồ thống kê"
    