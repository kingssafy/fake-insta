from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth import get_user_model
# Create your models here.

class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    like_users = models.ManyToManyField(get_user_model(), related_name='like_posts', blank=True)
    def __str__(self):
        return self.content
        
class Image(models. Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = ProcessedImageField(
        upload_to='posts/images',
        processors=[ResizeToFill(600, 600)],
        format = 'JPEG',
        options= {'quality': 90},
        )
        
class Comment(models.Model):
    content = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return "Comment: " + self.content