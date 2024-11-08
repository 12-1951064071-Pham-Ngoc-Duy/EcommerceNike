from django.db import models
from store.models import Product, Variation
from accounts.models import Account
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, verbose_name = "Mã giỏ hàng")
    cart_date_added = models.DateField(auto_now_add=True,verbose_name = "Ngày thêm giỏ hàng")
    class Meta:
        verbose_name = "Giỏ hàng"
        verbose_name_plural = "Giỏ hàng"

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,verbose_name = "Người dùng")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = "Sản phẩm")
    variations = models.ManyToManyField(Variation, blank=True,verbose_name = "Biến thể")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True,verbose_name = "Giỏ hàng")
    cart_item_quantity = models.IntegerField(verbose_name = "Số lượng")
    cart_item_is_active = models.BooleanField(default=True,verbose_name = "Sản phẩm hoạt động")
    class Meta:
        verbose_name = "Sản phẩm giỏ hàng"
        verbose_name_plural = "Sản phẩm giỏ hàng"


    @property
    def sub_total(self):
        return self.product.product_price * self.cart_item_quantity

    def __unicode__(self):
        return self.product
