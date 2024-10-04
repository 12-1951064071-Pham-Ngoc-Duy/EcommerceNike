
from django.urls import path
from .import views

urlpatterns = [
    path('', views.store , name='store'),
    path('category/<slug:category_slug_path>/', views.store , name='products_by_category'),
    path('category/<slug:category_slug_path>/<slug:product_slug_path>/', views.product_detail , name='product_detail'),
    path('search/', views.search, name='search')
]
