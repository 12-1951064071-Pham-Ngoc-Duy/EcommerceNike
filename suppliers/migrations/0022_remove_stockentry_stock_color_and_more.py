# Generated by Django 5.1.2 on 2024-11-17 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0021_remove_stockentry_stock_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockentry',
            name='stock_color',
        ),
        migrations.RemoveField(
            model_name='stockentry',
            name='stock_size',
        ),
        migrations.AddField(
            model_name='stockentry',
            name='stock_category',
            field=models.CharField(blank=True, choices=[('color', 'Màu sắc'), ('size', 'Kích cỡ')], max_length=100, null=True, verbose_name='Danh mục'),
        ),
        migrations.AddField(
            model_name='stockentry',
            name='stock_value',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Gía trị'),
        ),
    ]
