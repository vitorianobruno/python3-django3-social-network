from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    total_like = models.IntegerField()
    
    def __str__(self):
        return "POST_ID:" + str(self.pk) + " USER:" + str(self.user) + " LIKES:" + str(self.user_like)


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following_id = models.IntegerField()
    
    def __str__(self):
        return "USER:" + str(self.user) + " FOLLOWING:" + str(self.following_id)
        
    def serialize(self):
        return {
            "user": self.user,
            "following_id": self.following_id
        }
    
    
class Likes(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.post_id) + " USER_ID:" + str(self.user_id) + "/n"
        