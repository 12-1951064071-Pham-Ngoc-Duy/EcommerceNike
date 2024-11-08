# Generated by Django 5.1.2 on 2024-11-08 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_order_phone'),
        ('store', '0011_alter_variation_variation_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Đơn hàng', 'verbose_name_plural': 'Đơn hàng'},
        ),
        migrations.AlterModelOptions(
            name='orderproduct',
            options={'verbose_name': 'Sản phẩm đơn hàng', 'verbose_name_plural': 'Sản phẩm đơn hàng'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Thanh toán', 'verbose_name_plural': 'Thanh toán'},
        ),
        migrations.AlterField(
            model_name='order',
            name='order_address',
            field=models.CharField(max_length=50, verbose_name='Địa chỉ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Thành phố'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_country',
            field=models.CharField(choices=[('United States', 'United States'), ('Canada', 'Canada'), ('Mexico', 'Mexico'), ('United Kingdom', 'United Kingdom'), ('Germany', 'Germany'), ('France', 'France'), ('Italy', 'Italy'), ('Spain', 'Spain'), ('Netherlands', 'Netherlands'), ('Belgium', 'Belgium'), ('Austria', 'Austria'), ('Switzerland', 'Switzerland'), ('Sweden', 'Sweden'), ('Denmark', 'Denmark'), ('Norway', 'Norway'), ('Finland', 'Finland'), ('Ireland', 'Ireland'), ('Portugal', 'Portugal'), ('Greece', 'Greece'), ('Poland', 'Poland'), ('Czech Republic', 'Czech Republic'), ('Hungary', 'Hungary'), ('Romania', 'Romania'), ('Russia', 'Russia'), ('Australia', 'Australia'), ('New Zealand', 'New Zealand'), ('Japan', 'Japan'), ('South Korea', 'South Korea'), ('China', 'China'), ('Hong Kong', 'Hong Kong'), ('Taiwan', 'Taiwan'), ('Singapore', 'Singapore'), ('Malaysia', 'Malaysia'), ('Thailand', 'Thailand'), ('Indonesia', 'Indonesia'), ('Philippines', 'Philippines'), ('Vietnam', 'Vietnam'), ('India', 'India'), ('United Arab Emirates', 'United Arab Emirates'), ('Saudi Arabia', 'Saudi Arabia'), ('Turkey', 'Turkey'), ('South Africa', 'South Africa'), ('Brazil', 'Brazil'), ('Argentina', 'Argentina'), ('Chile', 'Chile'), ('Colombia', 'Colombia'), ('Peru', 'Peru'), ('Israel', 'Israel'), ('Egypt', 'Egypt')], max_length=50, null=True, verbose_name='Đất nước'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_email',
            field=models.EmailField(max_length=50, verbose_name='Thư điện tử'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_first_name',
            field=models.CharField(max_length=50, verbose_name='Tên đầu'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_ip',
            field=models.CharField(blank=True, max_length=20, verbose_name='Giao thức'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_is_ordered',
            field=models.BooleanField(default=False, verbose_name='Được đặt hàng'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_last_name',
            field=models.CharField(max_length=50, verbose_name='Tên cuối'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_note',
            field=models.CharField(blank=True, max_length=100, verbose_name='Ghi chú'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=20, verbose_name='Số đơn hàng'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_phone',
            field=models.CharField(max_length=50, verbose_name='Số điện thoại'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Đang xử lý', 'Đang xử lý'), ('Đóng gói', 'Đóng gói'), ('Chờ Nhận Hàng', 'Chờ Nhận Hàng'), ('Đang vận chuyển', 'Đang vận chuyển'), ('Tại Trung tâm Phân phối', 'Tại Trung tâm Phân phối'), ('Ra đi để giao hàng', 'Ra đi để giao hàng'), ('Đã giao', 'Đã giao'), ('Giao hàng không thành công', 'Giao hàng không thành công')], default='Đang xử lý', max_length=100, verbose_name='Trạng thái'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_tax',
            field=models.FloatField(verbose_name='Phí giao hàng'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_total',
            field=models.FloatField(verbose_name='Tổng'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Thời gian cập nhật'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_village',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Huyện'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment', verbose_name='Thanh toán'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Đơn hàng'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order_product_created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Thời gian tạo'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order_product_ordered',
            field=models.BooleanField(default=False, verbose_name='Được đặt hàng'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order_product_price',
            field=models.FloatField(verbose_name='Gía'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order_product_quantity',
            field=models.IntegerField(verbose_name='Số lượng'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order_product_updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Thời gian cập nhật'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment', verbose_name='Thanh toán'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Sản phẩm'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation', verbose_name='Biến thể'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount_paid',
            field=models.CharField(max_length=100, verbose_name='Tiền đã thanh toán'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Thời gian thanh toán'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(max_length=100, verbose_name='Mã thanh toán'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(max_length=100, verbose_name='Phương thức thanh toán'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(max_length=100, verbose_name='Trạng thái'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng'),
        ),
    ]
