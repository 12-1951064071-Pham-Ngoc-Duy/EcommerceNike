# Generated by Django 5.1.2 on 2024-11-08 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_alter_cart_cart_date_added_alter_cart_cart_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Nhóm quản lý giỏ hàng', 'verbose_name_plural': 'Giỏ hàng'},
        ),
        migrations.AlterModelOptions(
            name='cartitem',
            options={'verbose_name': 'Nhóm quản lý giỏ hàng', 'verbose_name_plural': 'Sản phẩm giỏ hàng'},
        ),
    ]