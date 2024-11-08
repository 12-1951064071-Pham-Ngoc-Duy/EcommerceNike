from django.db import models
from django.urls import reverse
from accounts.models import Account
from category.models import Category
from django.db.models import Avg, Count

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
    product_price = models.IntegerField(verbose_name = "Gía")
    product_images = models.ImageField(upload_to="photos/products",verbose_name = "Ảnh sản phẩm")
    product_stock = models.IntegerField(verbose_name = "Tồn kho")
    product_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Nam Nữ',verbose_name = "Giới tính")
    product_made_in = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default='Vietnam',verbose_name = "Nơi sản xuất")
    product_is_availabel = models.BooleanField(default=True,verbose_name = "Có sẵn")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name = "Danh mục")
    product_created_date = models.DateTimeField(auto_now_add=True,verbose_name = "Thời gian tạo")
    product_modifield_date = models.DateTimeField(auto_now=True,verbose_name = "Thời gian sửa đổi")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_products',verbose_name = "Nhà cung cấp")
    class Meta:
        verbose_name = 'Sản phẩm'
        verbose_name_plural = 'Sản phẩm'

    def count_colors(self):
        return Variation.objects.filter(product=self, variation_category='color', variation_is_active=True).count()

    def get_url(self):
        return reverse('product_detail', args=[self.category.category_slug, self.product_slug])

    def __str__(self):
        return self.product_name
    
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
            count = float(reviews['count'])
        return count
    
    def update_stock(self, quantity):
        self.product_stock += quantity
        self.save()

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', variation_is_active=True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', variation_is_active=True)

variation_category_choice = (
    ('color', 'Màu sắc'),
    ('size', 'Kích cỡ'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = "Sản phẩm")
    variation_category = models.CharField(max_length=100, choices=variation_category_choice,verbose_name = "Danh mục biến thể")
    variation_value = models.CharField(max_length=100,verbose_name = "Gía trị")
    variation_is_active = models.BooleanField(default=True,verbose_name = "Hoạt động")
    variation_created_date = models.DateTimeField(auto_now=True,verbose_name = "Thời gian tạo")
    class Meta:
        verbose_name = 'Biến thể'
        verbose_name_plural = 'Biến thể'

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
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