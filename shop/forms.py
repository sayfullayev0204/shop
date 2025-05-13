from django import forms
from .models import Comment, Reply, Rating

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your reply here...'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(),
        }
        labels = {
            'rating': 'Rate this product:',
        }
