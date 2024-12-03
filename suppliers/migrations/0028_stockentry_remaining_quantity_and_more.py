# Generated by Django 5.1.2 on 2024-12-02 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0027_alter_stockentry_stock_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockentry',
            name='remaining_quantity',
            field=models.IntegerField(default=0, verbose_name='Số lượng còn'),
        ),
        migrations.AlterField(
            model_name='stockentry',
            name='quantity',
            field=models.IntegerField(verbose_name='Số lượng nhập'),
        ),
    ]