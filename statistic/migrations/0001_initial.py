# Generated by Django 5.1.2 on 2024-11-19 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticsPlaceholder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Thống kê',
                'verbose_name_plural': 'Thống kê',
            },
        ),
    ]