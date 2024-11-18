from django.db import models
from django.urls import reverse
from accounts.models import Account
from category.models import Category
from django.db.models import Avg, Count
from django.apps import apps
from suppliers.models import Supplier

# Create your models here.

GENDER_CHOICES = [
        ('Nam', 'Nam'),
        ('Nữ', 'Nữ'),
        ('Trẻ em', 'Trẻ em'),
        ('Nam Nữ', 'Nam Nữ'),
    ]

COUNTRY_CHOICES = [
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


class Product(models.Model):
    product_name = models.CharField(max_length=200,verbose_name = "Tên sản phẩm")
    product_slug = models.SlugField(max_length=200, unique=True,verbose_name = "Tên nguồn sản phẩm")
    product_description = models.TextField(max_length=500, blank=True,verbose_name = "Mô tả sản phẩm")
    product_price = models.IntegerField(verbose_name = "Gía", default=0)
    product_images = models.ImageField(upload_to="photos/products",verbose_name = "Ảnh sản phẩm")
    product_stock = models.IntegerField(verbose_name = "Tồn kho", default=0)
    product_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Nam Nữ',verbose_name = "Giới tính")
    product_made_in = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default='Vietnam',verbose_name = "Nơi sản xuất")
    product_is_availabel = models.BooleanField(default=True,verbose_name = "Có sẵn")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name = "Danh mục")
    product_created_date = models.DateTimeField(auto_now_add=True,verbose_name = "Thời gian tạo")
    product_modifield_date = models.DateTimeField(auto_now=True,verbose_name = "Thời gian sửa đổi")
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_products',verbose_name = "Nhà cung cấp")
    class Meta:
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'

    def count_colors(self):
    # Tránh vòng lặp import
        Variation = apps.get_model('store', 'Variation')

    # Lấy tất cả các sản phẩm có cùng tên
        same_name_products = Product.objects.filter(product_name=self.product_name)

    # Lấy tất cả các màu sắc không trùng lặp (distinct) trong danh sách sản phẩm đó
        unique_colors = Variation.objects.filter(
            product__in=same_name_products,
            variation_category='color',
            variation_is_active=True
        ).values_list('variation_color', flat=True).distinct()

    # Trả về số lượng màu sắc
        return unique_colors.count()

    def get_url(self):
        return reverse('product_detail', args=[self.category.category_slug, self.product_slug])

    def __str__(self):
        return self.product_slug
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, review_status=True).aggregate(average=Avg('review_rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, review_status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
    
    def update_total_stock(self):
        total_stock = sum(variation.stock for variation in self.variation_set.all())
        self.product_stock = total_stock  # Giả sử bạn có trường `product_stock` để lưu tổng tồn kho
        self.save()

variation_category_choice = (
    ('color', 'Màu sắc'),
)
variation_value_choice = (
    ('size', 'Kích cỡ'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = "Sản phẩm")
    variation_category = models.CharField(max_length=100, choices=variation_category_choice,verbose_name = "Danh mục màu sắc", blank=True, null=True)
    variation_color = models.CharField(max_length=50, verbose_name="Màu sắc", blank=True,null=True)
    variation_value = models.CharField(max_length=100,verbose_name = "Danh mục kích cỡ",choices=variation_value_choice,blank=True, null=True)
    variation_size = models.CharField(max_length=50, verbose_name="Kích cỡ", blank=True,null=True)
    stock = models.IntegerField(default=0, verbose_name="Tồn kho")
    variation_is_active = models.BooleanField(default=True,verbose_name = "Hoạt động")
    variation_created_date = models.DateTimeField(auto_now=True,verbose_name = "Thời gian tạo")
    class Meta:
        verbose_name = 'Biến thể'
        verbose_name_plural = 'Biến thể'

    def save(self, *args, **kwargs):
        # Lưu biến thể
        super().save(*args, **kwargs)
        self.product.update_total_stock()

    def __str__(self):
        return f"{self.variation_category} - {self.variation_value}"
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = "Sản phẩm")
    user = models.ForeignKey(Account, on_delete=models.CASCADE,verbose_name = "Người dùng")
    review_subject = models.CharField(max_length=100, blank=True,verbose_name = "Tiêu đề đánh giá")
    review = models.TextField(max_length=500, blank=True,verbose_name = "Đánh giá")
    review_rating = models.FloatField(verbose_name = "Điểm đánh giá")
    review_ip = models.CharField(max_length=20, blank=True,verbose_name = "Giao thức")
    review_status = models.BooleanField(default=True,verbose_name = "Trạng thái")
    review_created_at = models.DateTimeField(auto_now_add=True,verbose_name = "Thời gian tạo")
    review_updated_at = models.DateTimeField(auto_now=True,verbose_name = "Thời gian cập nhật")
    class Meta:
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Đánh giá'

    def __str__(self):
        return self.review_subject
    

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE,verbose_name = "Sản phẩm")
    image_gallery = models.ImageField(upload_to='store/products', max_length=255,verbose_name = "Ảnh phụ sản phẩm")

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'Ảnh phụ sản phẩm'
        verbose_name_plural = 'Ảnh phụ sản phẩm'