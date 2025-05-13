from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='products_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('like/', views.like_product, name='like_product'),
    path('reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('search/', views.search_products, name='search_products'),
]
