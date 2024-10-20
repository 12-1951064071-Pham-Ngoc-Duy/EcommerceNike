# Generated by Django 3.1 on 2024-10-20 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_supplier'),
        ('suppliers', '0002_auto_20241020_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='other_costs',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='production_cost',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='shipping_cost',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='total_cost',
        ),
        migrations.CreateModel(
            name='StockEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('entry_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.supplier')),
            ],
        ),
    ]