# Generated by Django 5.1.2 on 2024-11-15 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_product_product_price_and_more'),
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
