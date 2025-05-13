# shop/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group
from .models import Category, Product, Comment, Reply, Rating, ProductView
from .forms2 import (
    CategoryForm, ProductForm, CommentForm, ReplyForm, RatingForm, ProductViewForm
)

admin.site.unregister(Group)

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    form = CategoryForm
    list_display = ['name', 'slug', 'created_products_count']
    list_filter = ['name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    actions = ['make_empty_description']

    def created_products_count(self, obj):
        return obj.products.count()
    created_products_count.short_description = 'Products Count'

    def make_empty_description(self, request, queryset):
        queryset.update(description='')
    make_empty_description.short_description = 'Clear Description'

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    form = ProductForm
    list_display = [
        'name', 'category', 'price', 'stock', 'available', 'total_likes',
        'average_rating', 'view_count', 'created'
    ]
    list_filter = ['category', 'available', 'created']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['owner', 'likes']
    list_editable = ['price', 'stock', 'available']
    ordering = ['-created']
    actions = ['make_unavailable', 'reset_likes']

    def make_unavailable(self, request, queryset):
        queryset.update(available=False)
    make_unavailable.short_description = 'Mark as Unavailable'

    def reset_likes(self, request, queryset):
        for product in queryset:
            product.likes.clear()
    reset_likes.short_description = 'Reset Likes'

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    form = CommentForm
    list_display = ['user', 'product', 'content_preview', 'created']
    list_filter = ['created', 'product']
    search_fields = ['content', 'user__username']
    raw_id_fields = ['user', 'product']
    ordering = ['-created']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Reply)
class ReplyAdmin(ModelAdmin):
    form = ReplyForm
    list_display = ['user', 'comment', 'content_preview', 'created']
    list_filter = ['created']
    search_fields = ['content', 'user__username']
    raw_id_fields = ['user', 'comment']
    ordering = ['created']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

@admin.register(Rating)
class RatingAdmin(ModelAdmin):
    form = RatingForm
    list_display = ['user', 'product', 'rating', 'created']
    list_filter = ['rating', 'created']
    search_fields = ['user__username', 'product__name']
    raw_id_fields = ['user', 'product']
    ordering = ['-created']

@admin.register(ProductView)
class ProductViewAdmin(ModelAdmin):
    form = ProductViewForm
    list_display = ['product', 'user', 'session_key', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['product__name', 'user__username', 'session_key']
    raw_id_fields = ['user', 'product']
    ordering = ['-timestamp']