from django.db import models

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
    
class StockEntry(models.Model):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE,verbose_name = "Sản phẩm")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,verbose_name = "Nhà cung cấp")
    quantity = models.IntegerField(verbose_name = "Số lượng")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name = "Đơn giá")
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name = "Tổng giá trị")  # Tổng giá trị
    entry_date = models.DateTimeField(auto_now_add=True,verbose_name = "Ngày nhập")
    class Meta:
        verbose_name = 'Nhập kho'
        verbose_name_plural = 'Nhập kho'

    def save(self, *args, **kwargs):
        # Tính tổng giá trị
        self.total_value = self.unit_price * self.quantity

        # Cập nhật tồn kho
        if self.pk:  # Nếu là bản cập nhật
            previous_entry = StockEntry.objects.get(pk=self.pk)
            stock_difference = self.quantity - previous_entry.quantity
            self.product.product_stock += stock_difference
        else:  # Nếu là bản thêm mới
            self.product.product_stock += self.quantity

        # Kiểm tra tồn kho không âm
        if self.product.product_stock < 0:
            raise ValueError("Tồn kho không thể âm. Kiểm tra lại số lượng nhập.")

        # Lưu sản phẩm
        self.product.save()  
        super().save(*args, **kwargs)  # Lưu mục StockEntry

    def __str__(self):
        return f"{self.product} - {self.quantity}"