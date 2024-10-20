from django.db import models
from django.urls import reverse
from accounts.models import Account
from category.models import Category
from django.db.models import Avg, Count

from suppliers.models import Supplier

# Create your models here.

GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('kid', 'Kid'),
        ('unisex', 'Unisex'),
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
    product_name = models.CharField(max_length=200)
    product_slug = models.SlugField(max_length=200, unique=True)
    product_description = models.TextField(max_length=500, blank=True)
    product_price = models.IntegerField()
    product_images = models.ImageField(upload_to="photos/products")
    product_stock = models.IntegerField()
    product_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    product_made_in = models.CharField(max_length=100, choices=COUNTRY_CHOICES, default='VN')
    product_is_availabel = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_created_date = models.DateTimeField(auto_now_add=True)
    product_modifield_date = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplied_products')

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
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    variation_is_active = models.BooleanField(default=True)
    variation_created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    review_subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    review_rating = models.FloatField()
    review_ip = models.CharField(max_length=20, blank=True)
    review_status = models.BooleanField(default=True)
    review_created_at = models.DateTimeField(auto_now_add=True)
    review_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_subject
    

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image_gallery = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'