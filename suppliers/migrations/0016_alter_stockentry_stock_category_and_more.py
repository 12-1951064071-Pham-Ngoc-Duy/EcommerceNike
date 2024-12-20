# Generated by Django 5.1.2 on 2024-11-16 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0015_rename_size_stockentry_stock_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockentry',
            name='stock_category',
            field=models.CharField(blank=True, choices=[('color', 'Màu sắc'), ('size', 'Kích cỡ')], max_length=100, null=True, verbose_name='Danh mục'),
        ),
        migrations.AlterField(
            model_name='stockentry',
            name='stock_value',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Gía trị'),
        ),
    ]
