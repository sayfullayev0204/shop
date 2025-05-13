# shop/forms2.py
from django import forms
from .models import Category, Product, Comment, Reply, Rating, ProductView

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'price', 'image', 'stock',
            'available', 'category', 'owner', 'likes'
        ]
        widgets = {
            'likes': forms.SelectMultiple(attrs={'size': 5}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['product', 'user', 'content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['comment', 'user', 'content']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['product', 'user', 'rating']

class ProductViewForm(forms.ModelForm):
    class Meta:
        model = ProductView
        fields = ['product', 'user', 'session_key']