# Generated by Django 5.1.2 on 2024-11-15 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0009_remove_stockentry_color_remove_stockentry_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockentry',
            name='variation_category',
            field=models.CharField(blank=True, choices=[('color', 'Màu sắc'), ('size', 'Kích cỡ')], max_length=100, null=True, verbose_name='Danh mục sản phẩm nhập'),
        ),
        migrations.AddField(
            model_name='stockentry',
            name='variation_value',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Giá trị sản phẩm nhập'),
        ),
    ]
