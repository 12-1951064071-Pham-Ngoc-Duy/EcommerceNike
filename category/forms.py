from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'category_slug', 'category_images']

    def clean_category_name(self):
        category_name = self.cleaned_data.get('category_name')
        if not category_name:
            raise forms.ValidationError("This field is required.")
        return category_name
    
    def clean_category_images(self):
        category_images = self.cleaned_data.get('category_images')
        if not category_images:
            raise forms.ValidationError("This field is required.")
        return category_images

    def clean_category_slug(self):
        category_slug = self.cleaned_data.get('category_slug')
        if not category_slug:
            raise forms.ValidationError("This field is required.")
        if ' ' in category_slug:
            raise forms.ValidationError("Slug cannot contain spaces.")
        if self.instance.pk: 
            if self.instance.category_slug == category_slug:
                return category_slug 
        if Category.objects.filter(category_slug=category_slug).exists():
            raise forms.ValidationError("This slug is already in use.")
        return category_slug
