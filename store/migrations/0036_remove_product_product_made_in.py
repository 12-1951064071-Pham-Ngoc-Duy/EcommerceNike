# Generated by Django 5.1.2 on 2024-11-26 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_remove_variation_variation_unit_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_made_in',
        ),
    ]
