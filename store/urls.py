
from django.urls import path
from .import views

urlpatterns = [
    path('', views.store , name='store'),
    path('category/<slug:category_slug_path>/', views.store , name='products_by_category'),
    path('category/<slug:category_slug_path>/<slug:product_slug_path>/', views.product_detail , name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>', views.submit_review, name='submit_review'),
    path('store/gender/<str:gender>/', views.store_by_gender, name='store_by_gender'),
]
