from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    following = models.ManyToManyField('User', blank=True, related_name='followed_by')
    post_liked = models.ManyToManyField('Post', blank=True, related_name='liked_by')
    

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='post')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.content[:25]}..."
    
    def serialize(self):
        return {
            'username': self.user.username,
            'content': self.content,
            'created_date': self.created_date,
            'likes': self.likes
        }