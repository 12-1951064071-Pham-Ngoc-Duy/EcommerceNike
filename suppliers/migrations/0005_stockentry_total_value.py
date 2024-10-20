# Generated by Django 3.1 on 2024-10-20 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0004_supplier_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockentry',
            name='total_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
