from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about', views.about_us, name='about_us'),
    path('customer-warrenty', views.customer_warrenty, name='customer_warrenty'),
    # path('warranty_list', views.warranty_list, name='warranty_list'),
    path('products', views.products, name='products'),
    path('products/<int:productId>/', views.product_detail, name='product_detail')
]