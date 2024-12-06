from django.db import models
from accounts.models import Account
from store.models import Product, Variation
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db.models import F
from django.db import transaction
from suppliers.models import StockEntry

COUNTRY_CHOICES = [
    ('Vietnam', 'Vietnam')
]

CITY_CHOICES = {
    'Vietnam': [
        ('An Giang', 'An Giang'),
    ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'),
    ('Bắc Giang', 'Bắc Giang'),
    ('Bắc Kạn', 'Bắc Kạn'),
    ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),
    ('Bình Định', 'Bình Định'),
    ('Bình Dương', 'Bình Dương'),
    ('Bình Phước', 'Bình Phước'),
    ('Bình Thuận', 'Bình Thuận'),
    ('Cà Mau', 'Cà Mau'),
    ('Cần Thơ', 'Cần Thơ'),
    ('Cao Bằng', 'Cao Bằng'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Đắk Lắk', 'Đắk Lắk'),
    ('Đắk Nông', 'Đắk Nông'),
    ('Điện Biên', 'Điện Biên'),
    ('Đồng Nai', 'Đồng Nai'),
    ('Đồng Tháp', 'Đồng Tháp'),
    ('Gia Lai', 'Gia Lai'),
    ('Hà Giang', 'Hà Giang'),
    ('Hà Nam', 'Hà Nam'),
    ('Hà Nội', 'Hà Nội'),
    ('Hà Tĩnh', 'Hà Tĩnh'),
    ('Hải Dương', 'Hải Dương'),
    ('Hải Phòng', 'Hải Phòng'),
    ('Hậu Giang', 'Hậu Giang'),
    ('Hòa Bình', 'Hòa Bình'),
    ('Hưng Yên', 'Hưng Yên'),
    ('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),
    ('Kon Tum', 'Kon Tum'),
    ('Lai Châu', 'Lai Châu'),
    ('Lâm Đồng', 'Lâm Đồng'),
    ('Lạng Sơn', 'Lạng Sơn'),
    ('Lào Cai', 'Lào Cai'),
    ('Long An', 'Long An'),
    ('Nam Định', 'Nam Định'),
    ('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),
    ('Ninh Thuận', 'Ninh Thuận'),
    ('Phú Thọ', 'Phú Thọ'),
    ('Phú Yên', 'Phú Yên'),
    ('Quảng Bình', 'Quảng Bình'),
    ('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),
    ('Quảng Ninh', 'Quảng Ninh'),
    ('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),
    ('Sơn La', 'Sơn La'),
    ('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),
    ('Thái Nguyên', 'Thái Nguyên'),
    ('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên Huế', 'Thừa Thiên Huế'),
    ('Tiền Giang', 'Tiền Giang'),
    ('TP. Hồ Chí Minh', 'TP. Hồ Chí Minh'),
    ('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),
    ('Vĩnh Long', 'Vĩnh Long'),
    ('Vĩnh Phúc', 'Vĩnh Phúc'),
    ('Yên Bái', 'Yên Bái')
    ]
}

VILLAGE_CHOICES = {
    'An Giang': [
        ('Tp. Long Xuyên', 'Tp. Long Xuyên'),
        ('Tp. Châu Đốc', 'Tp. Châu Đốc'),
        ('Thị xã Tân Châu', 'Thị xã Tân Châu'),
        ('Huyện An Phú', 'Huyện An Phú'),
        ('Huyện Châu Phú', 'Huyện Châu Phú'),
        ('Huyện Châu Thành', 'Huyện Châu Thành'),
        ('Huyện Chợ Mới', 'Huyện Chợ Mới'),
        ('Huyện Phú Tân', 'Huyện Phú Tân'),
        ('Huyện Thoại Sơn', 'Huyện Thoại Sơn'),
        ('Huyện Tịnh Biên', 'Huyện Tịnh Biên'),
        ('Huyện Tri Tôn', 'Huyện Tri Tôn'),
    ],
    'Bà Rịa - Vũng Tàu': [
        ('Tp. Vũng Tàu', 'Tp. Vũng Tàu'),
        ('Tp. Bà Rịa', 'Tp. Bà Rịa'),
        ('Thị xã Phú Mỹ', 'Thị xã Phú Mỹ'),
        ('Huyện Châu Đức', 'Huyện Châu Đức'),
        ('Huyện Côn Đảo', 'Huyện Côn Đảo'),
        ('Huyện Đất Đỏ', 'Huyện Đất Đỏ'),
        ('Huyện Long Điền', 'Huyện Long Điền'),
        ('Huyện Xuyên Mộc', 'Huyện Xuyên Mộc'),
    ],
    'Bắc Giang': [
        ('Tp. Bắc Giang', 'Tp. Bắc Giang'),
        ('Huyện Hiệp Hòa', 'Huyện Hiệp Hòa'),
        ('Huyện Lạng Giang', 'Huyện Lạng Giang'),
        ('Huyện Lục Nam', 'Huyện Lục Nam'),
        ('Huyện Lục Ngạn', 'Huyện Lục Ngạn'),
        ('Huyện Sơn Động', 'Huyện Sơn Động'),
        ('Huyện Tân Yên', 'Huyện Tân Yên'),
        ('Huyện Việt Yên', 'Huyện Việt Yên'),
        ('Huyện Yên Dũng', 'Huyện Yên Dũng'),
        ('Huyện Yên Thế', 'Huyện Yên Thế'),
    ],
    'Bắc Ninh': [
        ('Tp. Bắc Ninh', 'Tp. Bắc Ninh'),
        ('Thị xã Từ Sơn', 'Thị xã Từ Sơn'),
        ('Huyện Gia Bình', 'Huyện Gia Bình'),
        ('Huyện Lương Tài', 'Huyện Lương Tài'),
        ('Huyện Quế Võ', 'Huyện Quế Võ'),
        ('Huyện Thuận Thành', 'Huyện Thuận Thành'),
        ('Huyện Tiên Du', 'Huyện Tiên Du'),
        ('Huyện Yên Phong', 'Huyện Yên Phong'),
    ],
    'Cần Thơ': [
        ('Quận Ninh Kiều', 'Quận Ninh Kiều'),
        ('Quận Bình Thủy', 'Quận Bình Thủy'),
        ('Quận Cái Răng', 'Quận Cái Răng'),
        ('Quận Ô Môn', 'Quận Ô Môn'),
        ('Quận Thốt Nốt', 'Quận Thốt Nốt'),
        ('Huyện Cờ Đỏ', 'Huyện Cờ Đỏ'),
        ('Huyện Phong Điền', 'Huyện Phong Điền'),
        ('Huyện Thới Lai', 'Huyện Thới Lai'),
        ('Huyện Vĩnh Thạnh', 'Huyện Vĩnh Thạnh'),
    ],
    'Đà Nẵng': [
        ('Quận Hải Châu', 'Quận Hải Châu'),
        ('Quận Thanh Khê', 'Quận Thanh Khê'),
        ('Quận Sơn Trà', 'Quận Sơn Trà'),
        ('Quận Ngũ Hành Sơn', 'Quận Ngũ Hành Sơn'),
        ('Quận Liên Chiểu', 'Quận Liên Chiểu'),
        ('Quận Cẩm Lệ', 'Quận Cẩm Lệ'),
        ('Huyện Hòa Vang', 'Huyện Hòa Vang'),
        ('Huyện Hoàng Sa', 'Huyện Hoàng Sa'),
    ],
    'Hà Nội': [
        ('Quận Ba Đình', 'Quận Ba Đình'),
        ('Quận Hoàn Kiếm', 'Quận Hoàn Kiếm'),
        ('Quận Hai Bà Trưng', 'Quận Hai Bà Trưng'),
        ('Quận Đống Đa', 'Quận Đống Đa'),
        ('Quận Tây Hồ', 'Quận Tây Hồ'),
        ('Quận Cầu Giấy', 'Quận Cầu Giấy'),
        ('Quận Thanh Xuân', 'Quận Thanh Xuân'),
        ('Quận Hoàng Mai', 'Quận Hoàng Mai'),
        ('Quận Long Biên', 'Quận Long Biên'),
        ('Huyện Ba Vì', 'Huyện Ba Vì'),
        ('Huyện Chương Mỹ', 'Huyện Chương Mỹ'),
        ('Huyện Đan Phượng', 'Huyện Đan Phượng'),
        # Thêm các huyện còn lại
    ],
    'TP. Hồ Chí Minh': [
        ('Quận 1', 'Quận 1'),
        ('Quận 2', 'Quận 2'),
        ('Quận 3', 'Quận 3'),
        ('Quận 4', 'Quận 4'),
        ('Quận 5', 'Quận 5'),
        ('Quận 6', 'Quận 6'),
        ('Quận 7', 'Quận 7'),
        ('Quận 8', 'Quận 8'),
        ('Quận 9', 'Quận 9'),
        ('Quận 10', 'Quận 10'),
        ('Quận 11', 'Quận 11'),
        ('Quận 12', 'Quận 12'),
        ('Huyện Cần Giờ', 'Huyện Cần Giờ'),
        ('Huyện Nhà Bè', 'Huyện Nhà Bè'),
        # Thêm các huyện còn lại
    ],
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
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True,verbose_name = "Mã thanh toán")
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
    order_total = models.IntegerField(verbose_name = "Tổng")
    order_tax = models.IntegerField(verbose_name = "Phí giao hàng")
    order_status = models.CharField(max_length=100, choices=STATUS, default='Đang xử lý',verbose_name = "Trạng thái")
    order_ip = models.CharField(max_length=20, blank=True,verbose_name = "Giao thức")
    order_is_ordered = models.BooleanField(default=False,verbose_name = "Được đặt hàng")
    order_created_at = models.DateTimeField(auto_now_add=True,verbose_name = "Thời gian tạo")
    order_updated_at = models.DateTimeField(auto_now=True,verbose_name = "Thời gian cập nhật")
    class Meta:
        verbose_name = 'Đơn hàng'
        verbose_name_plural = 'Đơn hàng'

    def save(self, *args, **kwargs):
      if self.pk:  # Chỉ chạy khi cập nhật, không phải khi tạo mới
        old_order = Order.objects.get(pk=self.pk)

        # Kiểm tra nếu trạng thái đã thay đổi
        if (self.order_status == "Giao hàng không thành công" and not self.order_is_ordered) or \
           (old_order.order_status != self.order_status or old_order.order_is_ordered != self.order_is_ordered):

            # Lấy các sản phẩm trong đơn hàng
            order_products = OrderProduct.objects.filter(order=self)

            # Duyệt qua các sản phẩm trong đơn hàng
            for order_product in order_products:
                remaining_qty = order_product.order_product_quantity

                # Tìm các bản ghi kho tương ứng, sắp xếp theo ngày nhập (mới nhất trước)
                stock_entries = StockEntry.objects.filter(
                    product=order_product.product,
                    stock_color=order_product.variations.filter(variation_category='color').first().variation_color,
                    stock_size=order_product.variations.filter(variation_value='size').first().variation_size
                ).order_by('-entry_date')  # Sắp xếp theo ngày nhập, bản ghi mới nhập trước

                # Cập nhật kho
                for stock_entry in stock_entries:
                    if remaining_qty <= 0:
                        break

                    if self.order_status == "Giao hàng không thành công" and not self.order_is_ordered:
                        # Cộng số lượng vào kho (sử dụng bản ghi nhập kho mới nhất)
                        available_qty = stock_entry.quantity - stock_entry.remaining_quantity
                        update_qty = min(available_qty, remaining_qty)
                        stock_entry.remaining_quantity = F('remaining_quantity') + update_qty  # Cộng vào kho
                        remaining_qty -= update_qty

                        # Nếu số lượng còn lại trong kho = số lượng nhập (kho đã đầy), cộng vào bản ghi nhập sau
                        if stock_entry.remaining_quantity == stock_entry.quantity and remaining_qty > 0:
                            # Tìm bản ghi nhập kho sau (bản ghi nhập kho cũ nhất)
                            next_stock_entry = stock_entries.last()  # Lấy bản ghi nhập kho mới nhất
                            if next_stock_entry:
                                next_stock_entry.remaining_quantity = F('remaining_quantity') + remaining_qty
                                next_stock_entry.save()  # Cộng vào bản ghi nhập kho sau
                                remaining_qty = 0  # Đảm bảo rằng số lượng còn lại được đặt về 0

                    elif self.order_is_ordered:
                            update_qty = min(stock_entry.remaining_quantity, remaining_qty)
                            stock_entry.remaining_quantity = F('remaining_quantity') - update_qty  # Trừ từ kho
                            remaining_qty -= update_qty

                    stock_entry.save()  # Lưu lại bản ghi kho đã thay đổi

            # Tính toán lại chi phí
            self.update_statistics()

      super(Order, self).save(*args, **kwargs)





    
    def update_statistics(self):
        # Tính lại tổng doanh thu và chi phí
        total_revenue = Order.objects.filter(order_is_ordered=True).aggregate(total_revenue=Sum('order_total'))['total_revenue'] or 0
        total_cost = StockEntry.objects.aggregate(
            total_cost=Sum((F('quantity') - F('remaining_quantity')) * F('unit_price'))
        )['total_cost'] or 0
        
        # Tính lợi nhuận
        total_profit = total_revenue - total_cost
        # Cập nhật vào bảng thống kê hoặc gửi dữ liệu tới admin

    def full_name(self):
        return f'{self.order_first_name} {self.order_last_name}'
    
    def full_address(self):
        return f'{self.order_country} - {self.order_city} - {self.order_village}'

    def __str__(self):
        return self.order_number
    
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
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null = True,verbose_name = "Mã thanh toán")
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

class ReturnRequest(models.Model):

    RETURN_STATUS_CHOICES = [
        ("Đang xử lý", "Đang xử lý"),
        ("Đã chấp nhận", "Đã chấp nhận"),
        ("Đã từ chối", "Đã từ chối"),
        ("Hoàn thành", "Hoàn thành"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='return_requests', verbose_name="Đơn hàng")
    return_reason = models.TextField(max_length=255, verbose_name="Lý do trả hàng")
    status = models.CharField(max_length=50, choices=RETURN_STATUS_CHOICES, default="Đang xử lý", verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày yêu cầu")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = 'Yêu cầu trả hàng'
        verbose_name_plural = 'Yêu cầu trả hàng'

    def __str__(self):
        return f"Yêu cầu trả hàng #{self.id} - Đơn hàng: {self.order.order_number}"
    
class ReturnRequestImage(models.Model):
    return_request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name='images', verbose_name="Yêu cầu trả hàng")
    image = models.ImageField(upload_to='return_request_images/', verbose_name="Ảnh minh họa")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tải lên")

    class Meta:
        verbose_name = 'Ảnh minh họa'
        verbose_name_plural = 'Ảnh minh họa'

    def __str__(self):
        return f"Ảnh minh họa cho yêu cầu #{self.return_request.id}"
