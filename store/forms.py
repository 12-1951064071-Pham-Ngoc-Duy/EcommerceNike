from django import forms
from .models import ReviewRating, Variation
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if not product_name:
            raise forms.ValidationError('This field is required.')
        return product_name
    def clean_product_description(self):
        product_description = self.cleaned_data.get('product_description')
        if not product_description:
            raise forms.ValidationError('This field is required.')
        return product_description
    def clean_product_images(self):
        product_images = self.cleaned_data.get('product_images')
        if not product_images:
            raise forms.ValidationError('This field is required.')
        return product_images
    def clean_product_gender(self):
        product_gender = self.cleaned_data.get('product_gender')
        if not product_gender:
            raise forms.ValidationError('This field is required.')
        return product_gender
    def clean_product_made_in(self):
        product_made_in = self.cleaned_data.get('product_made_in')
        if not product_made_in:
            raise forms.ValidationError('This field is required.')
        return product_made_in
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required.')
        return category
    def clean_supplier(self):
        supplier = self.cleaned_data.get('supplier')
        if not supplier:
            raise forms.ValidationError('This field is required.')
        return supplier
    
    def clean_product_slug(self):
        product_slug = self.cleaned_data.get('product_slug')
        if not product_slug:
            raise forms.ValidationError('This field is required.')
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.product_slug == product_slug:
                return product_slug  # Không kiểm tra nếu email không thay đổi
        if Product.objects.filter(product_slug=product_slug).exists():
            raise forms.ValidationError("This product_slug is already in use.")
        return product_slug
    

    def clean_product_price(self):
        price = self.cleaned_data.get('product_price')
        if not price:
            raise forms.ValidationError('This field is required.')
        if price < 0:
            raise forms.ValidationError("Value product not minus")
        return price

    def clean_product_stock(self):
        stock = self.cleaned_data.get('product_stock')
        if not stock:
            raise forms.ValidationError('This field is required.')
        if stock is None or stock <= 0:
            raise forms.ValidationError("Value product not minus and more than 0")
        return stock

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review_subject', 'review', 'review_rating']

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation 
        fields = ['product','variation_category','variation_value']
    def clean(self):
        cleaned_data = super().clean()
        variation_category = cleaned_data.get('variation_category')
        variation_value = cleaned_data.get('variation_value')
        product = cleaned_data.get('product')

        if variation_category and variation_value and product:
            # Kiểm tra xem đã tồn tại bản ghi nào với cùng category và value cho sản phẩm này chưa
            existing_variation = Variation.objects.filter(
                product=product,
                variation_category=variation_category,
                variation_value=variation_value
            )

            # Bỏ qua bản ghi hiện tại nếu đang ở chế độ chỉnh sửa (edit)
            if self.instance.pk:
                existing_variation = existing_variation.exclude(pk=self.instance.pk)

            if existing_variation.exists():
                raise forms.ValidationError(
                    f"Variation with category '{variation_category}' "
                    f"and value '{variation_value}' already exists for this product."
                )

        return cleaned_data
    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not product:
            raise forms.ValidationError('This field is required.')
        return product
    def clean_variation_category(self):
        variation_category = self.cleaned_data.get('variation_category')
        if not variation_category:
            raise forms.ValidationError('This field is required.')
        return variation_category
    def clean_variation_value(self):
        variation_value = self.cleaned_data.get('variation_value')
        if not variation_value:
            raise forms.ValidationError('This field is required.')
        return variation_value
    
    
