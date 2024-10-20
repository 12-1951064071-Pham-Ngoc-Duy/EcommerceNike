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
    supplier_name = models.CharField(max_length=200)
    supplier_email = models.EmailField()
    supplier_phone = models.CharField(max_length=15, blank=True)
    supplier_address = models.TextField(blank=True)
    supplier_country = models.CharField(max_length=100, choices=NIKE_FACTORY_CHOICES)
    supplier_is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField('store.Product', blank=True, related_name='suppliers')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Lưu nhà cung cấp
        # Cập nhật trường supplier cho tất cả các sản phẩm
        for product in self.products.all():
            product.supplier = self
            product.save()

    def __str__(self):
        return self.supplier_name
    
class StockEntry(models.Model):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Đơn giá mỗi sản phẩm
    total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Tổng giá trị
    entry_date = models.DateTimeField(auto_now_add=True)

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