# Generated by Django 5.1.2 on 2024-11-15 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0011_remove_stockentry_variation_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockentry',
            name='color_stockentry',
        ),
        migrations.RemoveField(
            model_name='stockentry',
            name='size_stockentry',
        ),
    ]
