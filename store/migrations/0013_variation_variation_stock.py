# Generated by Django 5.1.2 on 2024-11-15 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_product_options_alter_productgallery_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='variation_stock',
            field=models.IntegerField(default=0, verbose_name='Tồn kho'),
        ),
    ]
