# Generated by Django 5.1.2 on 2024-12-04 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_account_mbs_level_discoundmbslevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='mbs_level',
            field=models.CharField(blank=True, choices=[('Vàng', 'Vàng'), ('Bạc', 'Bạc'), ('Đồng', 'Đồng')], default='', max_length=10, null=True, verbose_name='Hạng thành viên'),
        ),
    ]
