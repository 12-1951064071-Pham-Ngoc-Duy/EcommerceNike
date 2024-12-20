# Generated by Django 5.1.2 on 2024-11-17 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0020_alter_stockentry_stock_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockentry',
            name='stock_category',
        ),
        migrations.RemoveField(
            model_name='stockentry',
            name='stock_value',
        ),
        migrations.AddField(
            model_name='stockentry',
            name='stock_color',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Màu sắc'),
        ),
        migrations.AddField(
            model_name='stockentry',
            name='stock_size',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Kích cỡ'),
        ),
    ]
