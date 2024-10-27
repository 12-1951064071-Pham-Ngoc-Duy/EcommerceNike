from django import forms
from phonenumbers import NumberParseException
import phonenumbers
from .models import StockEntry, Supplier
import re

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'supplier_name', 'supplier_email', 'supplier_phone', 
            'supplier_address', 'supplier_country', 'supplier_is_active', 
            'products'
        ]

    def clean_supplier_email(self):
        supplier_email = self.cleaned_data.get('supplier_email')
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if not re.match(regex, supplier_email):
            raise forms.ValidationError("Invalid email format.")
        if not supplier_email:
            raise forms.ValidationError("This field is required.")

        # Kiểm tra tính tồn tại của email trong các nhà cung cấp khác
        existing_supplier = Supplier.objects.filter(supplier_email=supplier_email)
        if self.instance.pk:
            existing_supplier = existing_supplier.exclude(pk=self.instance.pk)

        if existing_supplier.exists():
            raise forms.ValidationError("This email is already in use.")

        return supplier_email

    def clean_supplier_name(self):
        supplier_name = self.cleaned_data.get('supplier_name')
        if not supplier_name:
            raise forms.ValidationError("This field is required.")
        return supplier_name

    def clean_supplier_country(self):
        supplier_country = self.cleaned_data.get('supplier_country')
        if not supplier_country:
            raise forms.ValidationError("This field is required.")
        return supplier_country

    def clean_supplier_phone(self):
        supplier_phone = self.cleaned_data.get('supplier_phone')
        if not supplier_phone:
            raise forms.ValidationError("This field is required.")

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not supplier_phone.startswith("+84"):
            raise forms.ValidationError("Phone number must start with '+84' followed by country code.")
    
        regex = r'^\+?\d+$'
        if not re.match(regex, supplier_phone):
            raise forms.ValidationError("Phone number must only number")
        
        # Kiểm tra chỉ chứa số sau dấu "+"
        if not supplier_phone[1:].isdigit():
            raise forms.ValidationError("Phone number must contain only digits after the country code.")
        
        # Kiểm tra độ dài hợp lệ (8-15 số)
        if len(supplier_phone[1:]) < 11:
            raise forms.ValidationError("Phone number must be between 8 and 15 digits after the country code.")
        
        # Kiểm tra tính hợp lệ bằng thư viện phonenumbers
        try:
            parsed_number = phonenumbers.parse(supplier_phone, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number for the given country code.")
        except NumberParseException:
            raise forms.ValidationError("Invalid phone number format.")
        
        # Kiểm tra số điện thoại đã tồn tại
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.supplier_phone == supplier_phone:
                return supplier_phone  # Không kiểm tra nếu số điện thoại không thay đổi
        if Supplier.objects.filter(supplier_phone=supplier_phone).exists():
            raise forms.ValidationError("Phone number already exists.")
        return supplier_phone
    
    def clean_supplier_address(self):
        supplier_address = self.cleaned_data.get('supplier_address')
        if not supplier_address:
            raise forms.ValidationError("This field is required.")
        return supplier_address
    
    def clean_products(self):
        products = self.cleaned_data.get('products')
        if not products:
            raise forms.ValidationError("This field is required.")
        return products


class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = [
            'product', 'supplier', 'quantity','unit_price',
        ]

    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not product:
            raise forms.ValidationError("This field is required.")
        return product
    def clean_supplier(self):
        supplier = self.cleaned_data.get('supplier')
        if not supplier:
            raise forms.ValidationError("This field is required.")
        return supplier
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        if not quantity:
            raise forms.ValidationError("This field is required.")
        return quantity
    def clean_unit_price(self):
        unit_price = self.cleaned_data.get('unit_price')
        if unit_price <= 0:
            raise forms.ValidationError("Unit price must be greater than zero.")
        if not unit_price:
            raise forms.ValidationError("This field is required.")
        return unit_price