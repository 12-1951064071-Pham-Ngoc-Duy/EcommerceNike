# Generated by Django 5.1.2 on 2024-11-16 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_variation_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(max_length=100, verbose_name='Màu sắc'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_value',
            field=models.CharField(max_length=100, verbose_name='Kích cỡ'),
        ),
    ]
