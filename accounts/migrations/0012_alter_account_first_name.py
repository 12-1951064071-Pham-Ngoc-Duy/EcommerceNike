# Generated by Django 5.1.2 on 2024-11-08 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_account_id_alter_userprofile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='Tên đầu'),
        ),
    ]
