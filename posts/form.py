from django.forms import ModelForm, FileInput
from .models import Post, Image, Comment
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content',]

        
class ImageForm(ModelForm):
    file = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True},))
    class Meta:
        model = Image
        fields = ['file',]
        # widgets = {
        #     'file': FileInput(attrs={'multiple': True}),
        # }

        
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
