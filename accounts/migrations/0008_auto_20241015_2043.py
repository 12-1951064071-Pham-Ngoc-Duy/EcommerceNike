# Generated by Django 3.1 on 2024-10-15 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20241015_2030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='state_address',
            new_name='account_address',
        ),
        migrations.AddField(
            model_name='account',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
