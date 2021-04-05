from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')


class CommentForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'rows': 1, 'placeholder': 'add a comment...', 'class': 'narrow-select'}))
    class Meta:
        model = Comment
        fields = ('text',)