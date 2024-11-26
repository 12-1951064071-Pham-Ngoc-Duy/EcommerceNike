# Generated by Django 5.1.2 on 2024-11-26 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_userprofile_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='country',
            field=models.CharField(choices=[('Vietnam', 'Vietnam')], max_length=50, null=True, verbose_name='Đất nước'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile_country',
            field=models.CharField(blank=True, choices=[('Vietnam', 'Vietnam')], max_length=20, verbose_name='Đất nước'),
        ),
    ]