# Generated by Django 5.1.2 on 2024-11-16 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_remove_variation_variation_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='variation_image',
            field=models.ImageField(blank=True, null=True, upload_to='variations/', verbose_name='Ảnh màu sắc'),
        ),
    ]
