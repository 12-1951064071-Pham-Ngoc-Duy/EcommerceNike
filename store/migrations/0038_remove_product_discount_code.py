# Generated by Django 5.1.2 on 2024-11-29 02:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_product_discount_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount_code',
        ),
    ]
