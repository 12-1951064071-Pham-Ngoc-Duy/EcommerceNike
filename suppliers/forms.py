from django import forms
from phonenumbers import NumberParseException
import phonenumbers

from store.models import Variation
from .models import StockEntry, Supplier
import re

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'supplier_name', 'supplier_email', 'supplier_phone', 
            'supplier_country','supplier_city', 'supplier_is_active', 
            'products',
        ]

    def clean_supplier_email(self):
        supplier_email = self.cleaned_data.get('supplier_email')
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if not re.match(regex, supplier_email):
            raise forms.ValidationError("Định dạng thư điện tử không hợp lệ.")
        if not supplier_email:
            raise forms.ValidationError("Trường này là bắt buộc")

        # Kiểm tra tính tồn tại của email trong các nhà cung cấp khác
        existing_supplier = Supplier.objects.filter(supplier_email=supplier_email)
        if self.instance.pk:
            existing_supplier = existing_supplier.exclude(pk=self.instance.pk)

        if existing_supplier.exists():
            raise forms.ValidationError("Thư điện tử này đã được sử dụng.")

        return supplier_email

    def clean_supplier_name(self):
        supplier_name = self.cleaned_data.get('supplier_name')
        if not supplier_name:
            raise forms.ValidationError("Trường này là bắt buộc")
        return supplier_name
    
    def clean_supplier_city(self):
        supplier_city = self.cleaned_data.get('supplier_city')
        if not supplier_city:
            raise forms.ValidationError("Trường này là bắt buộc")
        return supplier_city

    def clean_supplier_country(self):
        supplier_country = self.cleaned_data.get('supplier_country')
        if not supplier_country:
            raise forms.ValidationError("Trường này là bắt buộc")
        return supplier_country

    def clean_supplier_phone(self):
        supplier_phone = self.cleaned_data.get('supplier_phone')
        if not supplier_phone:
            raise forms.ValidationError("Trường này là bắt buộc")

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not supplier_phone.startswith("+"):
            raise forms.ValidationError("Số điện thoại phải bắt đầu bằng '+', sau đó là mã quốc gia.")
    
        regex = r'^\+?\d+$'
        if not re.match(regex, supplier_phone):
            raise forms.ValidationError("Số điện thoại chỉ được có số")
        
        # Kiểm tra chỉ chứa số sau dấu "+"
        if not supplier_phone[1:].isdigit():
            raise forms.ValidationError("Số điện thoại chỉ được chứa các chữ số sau mã quốc gia.")
        
        # # Kiểm tra độ dài hợp lệ (8-15 số)
        # if len(supplier_phone[1:]) < 11:
        #     raise forms.ValidationError("Phone number must be between 8 and 15 digits after the country code.")
        
        # Kiểm tra tính hợp lệ bằng thư viện phonenumbers
        try:
            parsed_number = phonenumbers.parse(supplier_phone, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Sai cấu trúc số điện thoại cho mã quốc gia")
        except NumberParseException:
            raise forms.ValidationError("Định dạng số điện thoại không hợp lệ.")
        
        # Kiểm tra số điện thoại đã tồn tại
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.supplier_phone == supplier_phone:
                return supplier_phone  # Không kiểm tra nếu số điện thoại không thay đổi
        if Supplier.objects.filter(supplier_phone=supplier_phone).exists():
            raise forms.ValidationError("Số điện thoại đã tồn tại.")
        return supplier_phone
    
    def clean_products(self):
        products = self.cleaned_data.get('products')
        if not products:
            raise forms.ValidationError("Trường này là bắt buộc")
        return products


class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = [
            'product', 'supplier', 'quantity','unit_price','stock_category','stock_color','stock_value','stock_size'
        ]
    
    def clean_stock_category(self):
        stock_category = self.cleaned_data.get('stock_category')
        if not stock_category:
            raise forms.ValidationError("Trường này là bắt buộc")
        return stock_category
        
    def clean_stock_color(self):
        stock_color = self.cleaned_data.get('stock_color')
        product = self.cleaned_data.get('product')
        
        if not stock_color:
            raise forms.ValidationError("Trường này là bắt buộc")
        
        # Kiểm tra màu sắc trong Variation
        if not Variation.objects.filter(product=product, variation_color=stock_color).exists():
            raise forms.ValidationError("Màu sắc không tồn tại với sản phẩm hãy thêm biến thể cho sản phẩm này")
        
        return stock_color
        
    def clean_stock_value(self):
        stock_value = self.cleaned_data.get('stock_value')
        if not stock_value:
            raise forms.ValidationError("Trường này là bắt buộc")
        return stock_value
        
    def clean_stock_size(self):
        stock_size = self.cleaned_data.get('stock_size')
        product = self.cleaned_data.get('product')
        
        if not stock_size:
            raise forms.ValidationError("Trường này là bắt buộc")
        
        # Kiểm tra màu sắc trong Variation
        if not Variation.objects.filter(product=product, variation_size=stock_size).exists():
            raise forms.ValidationError("Kích cỡ không tồn tại với sản phẩm hãy thêm biến thể cho sản phẩm này")
        
        return stock_size

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not product:
            raise forms.ValidationError("Trường này là bắt buộc")
        return product
    def clean_supplier(self):
        supplier = self.cleaned_data.get('supplier')
        product = self.cleaned_data.get('product')

        if not supplier:
            raise forms.ValidationError("Trường này là bắt buộc")

        if product and product.supplier != supplier:
            raise forms.ValidationError("Nhà cung cấp không đúng với sản phẩm. Vui lòng vào trang sản phẩm để xem thông tin")

        return supplier
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Số lượng phải lớn hơn 0.")
        if not quantity:
            raise forms.ValidationError("Trường này là bắt buộc")
        return quantity
    def clean_unit_price(self):
        unit_price = self.cleaned_data.get('unit_price')
        if unit_price <= 0:
            raise forms.ValidationError("Đơn giá phải lớn hơn 0.")
        if not unit_price:
            raise forms.ValidationError("Trường này là bắt buộc")
        return unit_price