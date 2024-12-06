from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('return_request/<str:order_number>/', views.return_request, name='return_request'),
    path('handle_return_request/<str:order_number>/', views.handle_return_request, name='handle_return_request'),
]
