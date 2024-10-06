# Generated by Django 3.1 on 2024-10-04 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20241004_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='village',
            name='city',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_country',
            field=models.CharField(choices=[('United States', 'United States'), ('Canada', 'Canada'), ('Mexico', 'Mexico'), ('United Kingdom', 'United Kingdom'), ('Germany', 'Germany'), ('France', 'France'), ('Italy', 'Italy'), ('Spain', 'Spain'), ('Netherlands', 'Netherlands'), ('Belgium', 'Belgium'), ('Austria', 'Austria'), ('Switzerland', 'Switzerland'), ('Sweden', 'Sweden'), ('Denmark', 'Denmark'), ('Norway', 'Norway'), ('Finland', 'Finland'), ('Ireland', 'Ireland'), ('Portugal', 'Portugal'), ('Greece', 'Greece'), ('Poland', 'Poland'), ('Czech Republic', 'Czech Republic'), ('Hungary', 'Hungary'), ('Romania', 'Romania'), ('Russia', 'Russia'), ('Australia', 'Australia'), ('New Zealand', 'New Zealand'), ('Japan', 'Japan'), ('South Korea', 'South Korea'), ('China', 'China'), ('Hong Kong', 'Hong Kong'), ('Taiwan', 'Taiwan'), ('Singapore', 'Singapore'), ('Malaysia', 'Malaysia'), ('Thailand', 'Thailand'), ('Indonesia', 'Indonesia'), ('Philippines', 'Philippines'), ('Vietnam', 'Vietnam'), ('India', 'India'), ('United Arab Emirates', 'United Arab Emirates'), ('Saudi Arabia', 'Saudi Arabia'), ('Turkey', 'Turkey'), ('South Africa', 'South Africa'), ('Brazil', 'Brazil'), ('Argentina', 'Argentina'), ('Chile', 'Chile'), ('Colombia', 'Colombia'), ('Peru', 'Peru'), ('Israel', 'Israel'), ('Egypt', 'Egypt')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_village',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='Village',
        ),
    ]