# Generated by Django 5.1.2 on 2024-11-25 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_variation_variation_color_variation_variation_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='variation_unit_price',
            field=models.IntegerField(default=0, verbose_name='Đơn giá'),
        ),
    ]