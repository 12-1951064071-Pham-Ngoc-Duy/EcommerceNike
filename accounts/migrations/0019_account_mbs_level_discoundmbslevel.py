# Generated by Django 5.1.2 on 2024-12-04 02:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_alter_account_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='mbs_level',
            field=models.CharField(blank=True, choices=[('Vàng', 'Vàng'), ('Bạc', 'Bạc'), ('Đồng', 'Đồng')], max_length=10, null=True, verbose_name='Hạng thành viên'),
        ),
        migrations.CreateModel(
            name='DiscoundMBSLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Mã giảm giá')),
                ('discount_percent', models.IntegerField(verbose_name='Phần trăm giảm giá')),
                ('is_used', models.BooleanField(default=False, verbose_name='Đã sử dụng')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('expires_at', models.DateTimeField(blank=True, null=True, verbose_name='Ngày hết hạn')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng')),
            ],
        ),
    ]
