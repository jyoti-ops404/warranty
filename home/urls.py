from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about', views.about_us, name='about_us'),
    path('calculator', views.calculator, name='calculator'),
    path('contact', views.contact_us, name='contact_us'),
    path('customer-warranty', views.customer_warranty, name='customer_warranty'),
    # path('products', views.products, name='products'),
    path('products/<int:productId>/', views.product_detail, name='product_detail'),
    path('download_pdf/<int:warranty_id>/', views.download_pdf, name='download_pdf'),
    path('category/<int:typeId>/', views.category_products, name='products'),
    path('products', views.all_products, name='all_products'),
]

