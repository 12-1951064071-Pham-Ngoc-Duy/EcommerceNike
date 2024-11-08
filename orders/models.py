from django.db import models
from accounts.models import Account
from store.models import Product, Variation
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth

# Create your models here.
# Create your models here.
COUNTRY_CHOICES = [
    ('United States', 'United States'),
    ('Canada', 'Canada'),
    ('Mexico', 'Mexico'),
    ('United Kingdom', 'United Kingdom'),
    ('Germany', 'Germany'),
    ('France', 'France'),
    ('Italy', 'Italy'),
    ('Spain', 'Spain'),
    ('Netherlands', 'Netherlands'),
    ('Belgium', 'Belgium'),
    ('Austria', 'Austria'),
    ('Switzerland', 'Switzerland'),
    ('Sweden', 'Sweden'),
    ('Denmark', 'Denmark'),
    ('Norway', 'Norway'),
    ('Finland', 'Finland'),
    ('Ireland', 'Ireland'),
    ('Portugal', 'Portugal'),
    ('Greece', 'Greece'),
    ('Poland', 'Poland'),
    ('Czech Republic', 'Czech Republic'),
    ('Hungary', 'Hungary'),
    ('Romania', 'Romania'),
    ('Russia', 'Russia'),
    ('Australia', 'Australia'),
    ('New Zealand', 'New Zealand'),
    ('Japan', 'Japan'),
    ('South Korea', 'South Korea'),
    ('China', 'China'),
    ('Hong Kong', 'Hong Kong'),
    ('Taiwan', 'Taiwan'),
    ('Singapore', 'Singapore'),
    ('Malaysia', 'Malaysia'),
    ('Thailand', 'Thailand'),
    ('Indonesia', 'Indonesia'),
    ('Philippines', 'Philippines'),
    ('Vietnam', 'Vietnam'),
    ('India', 'India'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('Turkey', 'Turkey'),
    ('South Africa', 'South Africa'),
    ('Brazil', 'Brazil'),
    ('Argentina', 'Argentina'),
    ('Chile', 'Chile'),
    ('Colombia', 'Colombia'),
    ('Peru', 'Peru'),
    ('Israel', 'Israel'),
    ('Egypt', 'Egypt'),
]

CITY_CHOICES = {
    'United States': [
        ('New York', 'New York'),
        ('Los Angeles', 'Los Angeles'),
        ('Chicago', 'Chicago'),
        # Thêm các thành phố khác của Mỹ
    ],
    'Canada': [
        ('Toronto', 'Toronto'),
        ('Vancouver', 'Vancouver'),
        ('Montreal', 'Montreal'),
        # Thêm các thành phố khác của Canada
    ],
    'Mexico': [
        ('Mexico City', 'Mexico City'),
        ('Guadalajara', 'Guadalajara'),
        ('Monterrey', 'Monterrey'),
        # Thêm các thành phố khác của Mexico
    ],
    'United Kingdom': [
        ('London', 'London'),
        ('Manchester', 'Manchester'),
        ('Birmingham', 'Birmingham'),
        # Thêm các thành phố khác của Vương Quốc Anh
    ],
    'Germany': [
        ('Berlin', 'Berlin'),
        ('Munich', 'Munich'),
        ('Hamburg', 'Hamburg'),
        # Thêm các thành phố khác của Đức
    ],
    'France': [
        ('Paris', 'Paris'),
        ('Marseille', 'Marseille'),
        ('Lyon', 'Lyon'),
        # Thêm các thành phố khác của Pháp
    ],
    'Italy': [
        ('Rome', 'Rome'),
        ('Milan', 'Milan'),
        ('Naples', 'Naples'),
        # Thêm các thành phố khác của Ý
    ],
    'Spain': [
        ('Madrid', 'Madrid'),
        ('Barcelona', 'Barcelona'),
        ('Valencia', 'Valencia'),
        # Thêm các thành phố khác của Tây Ban Nha
    ],
    # Tiếp tục thêm các lựa chọn thành phố cho các quốc gia khác...
}

VILLAGE_CHOICES = {
    'New York': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của New York
    ],
    'Los Angeles': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Los Angeles
    ],
    'Toronto': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Toronto
    ],
    'Vancouver': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Vancouver
    ],
    'Mexico City': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Mexico City
    ],
    'London': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của London
    ],
    'Berlin': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Berlin
    ],
    'Paris': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Paris
    ],
    'Rome': [
        ('Village1', 'Village 1'),
        ('Village2', 'Village 2'),
        # Thêm các làng khác của Rome
    ],
    # Tiếp tục thêm các lựa chọn làng cho các thành phố khác...
}
    
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name = "Người dùng")
    payment_id = models.CharField(max_length=100,verbose_name = "Mã thanh toán")
    payment_method = models.CharField(max_length=100,verbose_name = "Phương thức thanh toán")
    amount_paid  = models.CharField(max_length=100,verbose_name = "Tiền đã thanh toán")
    status = models.CharField(max_length=100,verbose_name = "Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name = "Thời gian thanh toán")
    class Meta:
        verbose_name = 'Thanh toán'
        verbose_name_plural = 'Thanh toán'

    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS = (
        ("Đang xử lý", "Đang xử lý"),
    ("Đóng gói", "Đóng gói"),
    ("Chờ Nhận Hàng", "Chờ Nhận Hàng"),
    ("Đang vận chuyển", "Đang vận chuyển"),
    ("Tại Trung tâm Phân phối", "Tại Trung tâm Phân phối"),
    ("Ra đi để giao hàng", "Ra đi để giao hàng"),
    ("Đã giao", "Đã giao"),
    ("Giao hàng không thành công", "Giao hàng không thành công"),
    )
    

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True,verbose_name = "Người dùng")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True,verbose_name = "Thanh toán")
    order_number = models.CharField(max_length=20,verbose_name = "Số đơn hàng")
    order_first_name = models.CharField(max_length=50,verbose_name = "Tên đầu")
    order_last_name = models.CharField(max_length=50,verbose_name = "Tên cuối")
    order_phone = models.CharField(max_length=50,verbose_name = "Số điện thoại")
    order_email = models.EmailField(max_length=50,verbose_name = "Thư điện tử")
    order_address = models.CharField(max_length=50,verbose_name = "Địa chỉ")
    order_country = models.CharField(max_length=50,null=True, choices=COUNTRY_CHOICES,verbose_name = "Đất nước")
    order_city = models.CharField(max_length=50, blank=True, null=True,verbose_name = "Thành phố")
    order_village = models.CharField(max_length=50, blank=True, null=True,verbose_name = "Huyện")
    order_note = models.CharField(max_length=100, blank=True,verbose_name = "Ghi chú")
    order_total = models.FloatField(verbose_name = "Tổng")
    order_tax = models.FloatField(verbose_name = "Phí giao hàng")
    order_status = models.CharField(max_length=100, choices=STATUS, default='Đang xử lý',verbose_name = "Trạng thái")
    order_ip = models.CharField(max_length=20, blank=True,verbose_name = "Giao thức")
    order_is_ordered = models.BooleanField(default=False,verbose_name = "Được đặt hàng")
    order_created_at = models.DateTimeField(auto_now_add=True,verbose_name = "Thời gian tạo")
    order_updated_at = models.DateTimeField(auto_now=True,verbose_name = "Thời gian cập nhật")
    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'

    def full_name(self):
        return f'{self.order_first_name} {self.order_last_name}'
    
    def full_address(self):
        return f'{self.order_country} - {self.order_city} - {self.order_village}'

    def __str__(self):
        return self.order_first_name
    
    @classmethod
    def doanh_thu_hang_ngay(cls):
        return cls.objects.annotate(ngay=TruncDay('order_created_at')) \
                          .values('ngay') \
                          .annotate(tong_doanh_thu=Sum('order_total'))

    @classmethod
    def doanh_thu_hang_thang(cls):
        return cls.objects.annotate(thang=TruncMonth('order_created_at')) \
                          .values('thang') \
                          .annotate(tong_doanh_thu=Sum('order_total'))
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,verbose_name = "Đơn hàng")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null = True,verbose_name = "Thanh toán")
    user = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name = "Người dùng")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = "Sản phẩm")
    variations = models.ManyToManyField(Variation, blank=True,verbose_name = "Biến thể")
    order_product_quantity = models.IntegerField(verbose_name = "Số lượng")
    order_product_price = models.FloatField(verbose_name = "Gía")
    order_product_ordered = models.BooleanField(default=False,verbose_name = "Được đặt hàng")
    order_product_created_at = models.DateTimeField(auto_now_add=True,verbose_name = "Thời gian tạo")
    order_product_updated_at = models.DateTimeField(auto_now=True,verbose_name = "Thời gian cập nhật")
    class Meta:
        verbose_name = 'Sản phẩm đơn hàng'
        verbose_name_plural = 'Sản phẩm đơn hàng'

    def __str__(self):
        return self.product.product_name

