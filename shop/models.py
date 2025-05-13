from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories', blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products_by_category', kwargs={'category_slug': self.slug})
    class Meta:
        verbose_name = "Turkumlar"
        verbose_name_plural = "Turkumlar"


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products')
    stock = models.PositiveIntegerField(default=1)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_products', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_products')
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def total_likes(self):
        return self.likes.count()

    def average_rating(self):
        ratings = Rating.objects.filter(product=self).aggregate(avg_rating=Avg('rating'))
        return ratings['avg_rating'] if ratings['avg_rating'] else 0

    def get_star_percentage(self):
        avg = self.average_rating()
        return int((avg / 5) * 100) if avg else 0
    
    class Meta:
        verbose_name = "Mahsulotlar"
        verbose_name_plural = "Mahsulotlar"

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'Comment by {self.settings.AUTH_USER_MODEL.username} on {self.product.name}'

    class Meta:
        verbose_name = "Sharhlar"
        verbose_name_plural = "Sharhlar"

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
        verbose_name_plural = 'Replies'
    
    def __str__(self):
        return f'Reply by {self.user.username} to {self.comment.user.username}'

    class Meta:
        verbose_name = "Qayta javob"
        verbose_name_plural = "Qayta javob"
        
class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent')
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'user')  # Each user can rate a product only once
        
    def __str__(self):
        return f'{self.user.username} rated {self.product.name} {self.rating} stars'

    class Meta:
        
        verbose_name = "Reyting"
        verbose_name_plural = "Reyting"

class ProductView(models.Model):
    """Track unique views for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # For authenticated users
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For anonymous users
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [
            ['product', 'user'],  # Each authenticated user counts as one view per product
            ['product', 'session_key']  # Each session counts as one view per product
        ]
    
    def __str__(self):
        if self.user:
            return f'{self.product.name} viewed by {self.user.first_name}'
        return f'{self.product.name} viewed by session {self.session_key}'

    class Meta:
        
        verbose_name = "Mahsulotlar ko'rish"
        verbose_name_plural = "Mahsulotlar ko'rish"