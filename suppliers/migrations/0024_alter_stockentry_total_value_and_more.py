# Generated by Django 5.1.2 on 2024-11-25 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0023_stockentry_stock_color_stockentry_stock_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockentry',
            name='total_value',
            field=models.IntegerField(default=0, verbose_name='Tổng giá trị'),
        ),
        migrations.AlterField(
            model_name='stockentry',
            name='unit_price',
            field=models.IntegerField(verbose_name='Đơn giá'),
        ),
    ]