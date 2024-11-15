# Generated by Django 5.1.2 on 2024-11-15 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0007_alter_stockentry_options_alter_supplier_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockentry',
            name='color',
            field=models.CharField(blank=True, default='Không có màu sắc', max_length=100, verbose_name='Màu sắc'),
        ),
        migrations.AddField(
            model_name='stockentry',
            name='size',
            field=models.CharField(blank=True, default='Không có kích cỡ', max_length=100, verbose_name='Kích cỡ'),
        ),
    ]