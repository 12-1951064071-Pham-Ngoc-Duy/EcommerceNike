# Generated by Django 5.1.2 on 2024-11-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_product_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_gender',
            field=models.CharField(choices=[('Nam', 'Nam'), ('Nữ', 'Nữ'), ('Trẻ em', 'Trẻ em'), ('Nam Nữ', 'Nam Nữ')], default='Nam Nữ', max_length=10),
        ),
    ]
