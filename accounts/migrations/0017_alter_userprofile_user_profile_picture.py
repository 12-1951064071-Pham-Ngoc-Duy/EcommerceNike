# Generated by Django 5.1.2 on 2024-11-10 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_userprofile_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='userprofile', verbose_name='Ảnh hồ sơ'),
        ),
    ]