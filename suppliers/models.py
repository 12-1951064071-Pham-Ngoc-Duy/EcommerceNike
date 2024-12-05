from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db.models import Sum

# Create your models here.
NIKE_FACTORY_CHOICES = [
    ('Vietnam', 'Vietnam'),
]
CITY_CHOICES = {
    'Vietnam': [
        ('TP. Hồ Chí Minh', 'TP. Hồ Chí Minh'),
        ('Bình Dương', 'Bình Dương'),
        ('Đồng Nai', 'Đồng Nai'),
        ('Tây Ninh', 'Tây Ninh'),
        ('Đà Nẵng', 'Đà Nẵng'),
        ('Quảng Nam', 'Quảng Nam'),
    ]
}

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=200,verbose_name = "Tên nhà cung cấp")
    supplier_email = models.EmailField(verbose_name = "Thư điện tử")
    supplier_phone = models.CharField(max_length=15, blank=True,verbose_name = "Số điện thoại")
    supplier_country = models.CharField(max_length=100, choices=NIKE_FACTORY_CHOICES,verbose_name = "Đất nước")
    supplier_city = models.CharField(max_length=100, choices=CITY_CHOICES,verbose_name = "Thành phố",blank=True, null=True)
    supplier_is_active = models.BooleanField(default=True,verbose_name = "Hoạt động")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name = "Thời gian tạo")
    updated_at = models.DateTimeField(auto_now=True,verbose_name = "Thời gian cập nhật")
    products = models.ManyToManyField('store.Product', blank=True, related_name='suppliers',verbose_name = "Sản phẩm")
    class Meta:
        verbose_name = 'Nhà cung cấp'
        verbose_name_plural = 'Nhà cung cấp'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Lưu nhà cung cấp
        # Cập nhật trường supplier cho tất cả các sản phẩm
        for product in self.products.all():
            product.supplier = self
            product.save()

    def __str__(self):
        return self.supplier_name

stockentry_category_choice = (
    ('color', 'Màu sắc'),
)
stockentry_value_choice = (
    ('size', 'Kích cỡ'),
)
    
class StockEntry(models.Model):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE,verbose_name = "Tên nguồn sản phẩm")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,verbose_name = "Nhà cung cấp")
    quantity = models.IntegerField(verbose_name = "Số lượng nhập")
    remaining_quantity = models.IntegerField(verbose_name="Số lượng còn", default=0)
    stock_category = models.CharField(max_length=100, verbose_name="Danh mục màu sắc",choices=stockentry_category_choice,blank=True,null=True)
    stock_color = models.CharField(max_length=50, verbose_name="Màu sắc", blank=True,null=True)
    stock_value = models.CharField(max_length=100, verbose_name="Danh mục kích cỡ",choices=stockentry_value_choice, blank=True, null=True)
    stock_size = models.CharField(max_length=50, verbose_name="Kích cỡ", blank=True,null=True)
    unit_price = models.IntegerField(verbose_name = "Đơn giá")
    total_value = models.IntegerField(default=0, verbose_name = "Tổng giá trị")  # Tổng giá trị
    entry_date = models.DateTimeField(auto_now_add=True,verbose_name = "Ngày nhập")
    class Meta:
        verbose_name = 'Nhập kho'
        verbose_name_plural = 'Nhập kho'

    def save(self, *args, **kwargs):
    # Tính tổng giá trị cho stock entry
        self.total_value = self.unit_price * self.quantity

    # Nếu là bản ghi mới, đặt remaining_quantity bằng quantity
        if not self.pk:
            self.remaining_quantity = self.quantity

        super().save(*args, **kwargs)  # Lưu bản ghi kho trước

    # Cập nhật lại stock trong Variation
        self.update_variation_stock()

    # Cập nhật tổng tồn kho trong Product
        self.product.update_total_stock()

    def update_variation_stock(self):
        Variation = apps.get_model('store', 'Variation')

    # Tìm biến thể tương ứng với màu sắc và kích cỡ
        variation = Variation.objects.filter(
        product=self.product,
        variation_category='color',
        variation_color=self.stock_color,
        variation_value='size',
        variation_size=self.stock_size,
        variation_is_active=True
    ).first()

        if variation:
        # Tổng hợp tất cả remaining_quantity từ StockEntry tương ứng với biến thể này
            total_remaining_quantity = StockEntry.objects.filter(
                product=self.product,
                stock_color=self.stock_color,
                stock_size=self.stock_size
            ).aggregate(total_remaining=Sum('remaining_quantity'))['total_remaining'] or 0

        # Cập nhật giá trị tồn kho cho biến thể
            variation.stock = total_remaining_quantity
            variation.save()

    def __str__(self):
        return f"{self.product} - {self.quantity}"