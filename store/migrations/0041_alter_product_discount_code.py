# Generated by Django 5.1.2 on 2024-11-29 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0040_alter_product_discount_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_code',
            field=models.FloatField(default=0, verbose_name='Mã giảm giá'),
        ),
    ]