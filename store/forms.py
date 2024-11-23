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
            raise forms.ValidationError('Trường này là bắt buộc')
        return product_name
    def clean_product_description(self):
        product_description = self.cleaned_data.get('product_description')
        if not product_description:
            raise forms.ValidationError('Trường này là bắt buộc')
        return product_description
    def clean_product_images(self):
        product_images = self.cleaned_data.get('product_images')
        if not product_images:
            raise forms.ValidationError('Trường này là bắt buộc')
        return product_images
    def clean_product_gender(self):
        product_gender = self.cleaned_data.get('product_gender')
        if not product_gender:
            raise forms.ValidationError('Trường này là bắt buộc')
        return product_gender
    def clean_product_made_in(self):
        product_made_in = self.cleaned_data.get('product_made_in')
        if not product_made_in:
            raise forms.ValidationError('Trường này là bắt buộc')
        return product_made_in
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('Trường này là bắt buộc')
        return category
    def clean_supplier(self):
        supplier = self.cleaned_data.get('supplier')
        if not supplier:
            raise forms.ValidationError('Trường này là bắt buộc')
        return supplier
    
    def clean_product_slug(self):
        product_slug = self.cleaned_data.get('product_slug')
        if not product_slug:
            raise forms.ValidationError('Trường này là bắt buộc')
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.product_slug == product_slug:
                return product_slug  # Không kiểm tra nếu email không thay đổi
        if Product.objects.filter(product_slug=product_slug).exists():
            raise forms.ValidationError("Nguồn sản phẩm đã tồn tại")
        return product_slug

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review_subject', 'review', 'review_rating']

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation 
        fields = ['product','variation_category','variation_value','variation_color','variation_size']
    def clean(self):
        cleaned_data = super().clean()
        variation_color = cleaned_data.get('variation_color')
        variation_size = cleaned_data.get('variation_size')
        product = cleaned_data.get('product')

        if variation_color and variation_size and product:
            # Kiểm tra xem đã tồn tại biến thể với cùng màu sắc và kích cỡ cho sản phẩm này chưa
            existing_variation = Variation.objects.filter(
                product=product,
                variation_color=variation_color,
                variation_size=variation_size
            )

            # Bỏ qua bản ghi hiện tại nếu đang ở chế độ chỉnh sửa
            if self.instance.pk:
                existing_variation = existing_variation.exclude(pk=self.instance.pk)

            if existing_variation.exists():
                raise forms.ValidationError(
                    f"Biến thể với màu sắc '{variation_color}' và kích cỡ '{variation_size}' đã tồn tại cho sản phẩm này."
                )

        return cleaned_data
    def clean_product(self):
        product = self.cleaned_data.get('product')
        if not product:
            raise forms.ValidationError('Trường này là bắt buộc')
        return product
    def clean_variation_category(self):
        variation_category = self.cleaned_data.get('variation_category')
        if not variation_category:
            raise forms.ValidationError('Trường này là bắt buộc')
        return variation_category
    def clean_variation_value(self):
        variation_value = self.cleaned_data.get('variation_value')
        if not variation_value:
            raise forms.ValidationError('Trường này là bắt buộc')
        return variation_value
    def clean_variation_color(self):
        variation_color = self.cleaned_data.get('variation_color')
        if not variation_color:
            raise forms.ValidationError('Trường này là bắt buộc')
        return variation_color
    def clean_variation_size(self):
        variation_size = self.cleaned_data.get('variation_size')
        if not variation_size:
            raise forms.ValidationError('Trường này là bắt buộc')
        return variation_size
    
    
