# Generated by Django 3.1 on 2024-10-15 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_account_account_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='state',
            new_name='place',
        ),
    ]