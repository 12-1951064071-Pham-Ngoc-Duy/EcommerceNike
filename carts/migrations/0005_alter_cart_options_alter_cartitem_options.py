# Generated by Django 5.1.2 on 2024-11-08 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_alter_cart_options_alter_cartitem_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Giỏ hàng', 'verbose_name_plural': 'Giỏ hàng'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Sản phẩm giỏ hàng', 'verbose_name_plural': 'Sản phẩm giỏ hàng'},
        ),
    ]
