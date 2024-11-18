from django.db import models
from django.apps import apps
from django.core.exceptions import ValidationError

# Create your models here.
NIKE_FACTORY_CHOICES = [
    ('Vietnam', 'Vietnam'),
    ('China', 'China'),
    ('Indonesia', 'Indonesia'),
    ('Thailand', 'Thailand'),
    ('India', 'India'),
    ('Philippines', 'Philippines'),
    ('Pakistan', 'Pakistan'),
    ('Taiwan', 'Taiwan'),
    ('Malaysia', 'Malaysia'),
    ('Bangladesh', 'Bangladesh'),
    ('Mexico', 'Mexico'),
    ('Italy', 'Italy'),
    ('Brazil', 'Brazil'),
    ('Egypt', 'Egypt'),
    ('Turkey', 'Turkey'),
    ('South Korea', 'South Korea'),
    ('United States', 'United States'),
    ('Cambodia', 'Cambodia'),
]

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=200,verbose_name = "Tên nhà cung cấp")
    supplier_email = models.EmailField(verbose_name = "Thư điện tử")
    supplier_phone = models.CharField(max_length=15, blank=True,verbose_name = "Số điện thoại")
    supplier_address = models.TextField(blank=True,verbose_name = "Địa chỉ")
    supplier_country = models.CharField(max_length=100, choices=NIKE_FACTORY_CHOICES,verbose_name = "Đất nước")
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
    quantity = models.IntegerField(verbose_name = "Số lượng")
    stock_category = models.CharField(max_length=100, verbose_name="Danh mục màu sắc",choices=stockentry_category_choice,blank=True,null=True)
    stock_color = models.CharField(max_length=50, verbose_name="Màu sắc", blank=True,null=True)
    stock_value = models.CharField(max_length=100, verbose_name="Danh mục kích cỡ",choices=stockentry_value_choice, blank=True, null=True)
    stock_size = models.CharField(max_length=50, verbose_name="Kích cỡ", blank=True,null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name = "Đơn giá")
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name = "Tổng giá trị")  # Tổng giá trị
    entry_date = models.DateTimeField(auto_now_add=True,verbose_name = "Ngày nhập")
    class Meta:
        verbose_name = 'Nhập kho'
        verbose_name_plural = 'Nhập kho'

    def save(self, *args, **kwargs):
    # Tính tổng giá trị
        self.total_value = self.unit_price * self.quantity

    # Lấy model Variation để tránh vòng lặp import
        Variation = apps.get_model('store', 'Variation')

    # Tính toán chênh lệch tồn kho
        stock_difference = self.quantity - self._get_previous_quantity()

    # Xử lý cho màu sắc và kích cỡ
        if self.stock_color and self.stock_size:
        # Tìm kiếm biến thể với cả màu sắc và kích cỡ
            variation = Variation.objects.filter(
                product=self.product,
                variation_category='color',
                variation_color=self.stock_color,
                variation_value='size',
                variation_size=self.stock_size,
                variation_is_active=True
            ).first()

            if not variation:
                raise ValidationError(
                    f"Biến thể với màu '{self.stock_color}' và kích cỡ '{self.stock_size}' không hợp lệ!"
                )

        # Cập nhật tồn kho cho biến thể
            variation.stock += stock_difference
            variation.save()

    # Cập nhật tổng tồn kho sản phẩm
        self.product.update_total_stock()
        self.product.save()

    # Lưu StockEntry
        super().save(*args, **kwargs)


    def _get_previous_quantity(self):
        """
        Lấy số lượng của StockEntry trước đó để tính toán chênh lệch tồn kho.
        """
        if self.pk:
            try:
                previous_entry = StockEntry.objects.get(pk=self.pk)
                return previous_entry.quantity
            except StockEntry.DoesNotExist:
                return 0
        return 0

    def __str__(self):
        return f"{self.product} - {self.quantity}"