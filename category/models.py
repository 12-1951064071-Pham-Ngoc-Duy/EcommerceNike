from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True, verbose_name = "Tên danh mục")
    category_slug = models.SlugField(max_length=100, unique=True, verbose_name = "Tên nguồn danh mục")
    category_images = models.ImageField(upload_to='photos/categories', blank=True,verbose_name = "Ảnh danh mục")

    class Meta:
        verbose_name = 'Danh mục'
        verbose_name_plural = 'Danh mục'

    def get_url(self):
        return reverse('products_by_category', args=[self.category_slug])

    def __str__(self):
        return self.category_name