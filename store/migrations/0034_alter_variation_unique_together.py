# Generated by Django 5.1.2 on 2024-11-17 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_variation_variation_color_variation_variation_size_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='variation',
            unique_together={('product', 'variation_category', 'variation_value')},
        ),
    ]
