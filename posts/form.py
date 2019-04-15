from django.forms import ModelForm, FileInput
from .models import Post, Image
from django import forms

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content',]
        
class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['file',]
        widgets = {
            'file': FileInput(attrs={'multiple': True}),
        }