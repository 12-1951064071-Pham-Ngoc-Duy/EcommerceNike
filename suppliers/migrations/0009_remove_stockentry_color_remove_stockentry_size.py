# Generated by Django 5.1.2 on 2024-11-15 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0008_stockentry_color_stockentry_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockentry',
            name='color',
        ),
        migrations.RemoveField(
            model_name='stockentry',
            name='size',
        ),
    ]
