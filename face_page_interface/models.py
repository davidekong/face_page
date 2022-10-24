from distutils.command.upload import upload
from email.policy import default
from statistics import mode
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CustomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=100000, default="Hi, i'm amazing!!")
    picture = models.ImageField(upload_to='face_page/media/images')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='face_page/media/images')
    title = models.CharField(max_length=50, default='')
    text = models.CharField(max_length=100000)
    likes = models.IntegerField(default=0)
    users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts')

class CommentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    likes = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
