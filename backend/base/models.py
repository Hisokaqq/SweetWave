from email.policy import default
from unicodedata import decimal
from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    artist = models.CharField(max_length=200, null=True, blank=True)
    cover = models.ImageField(null=True, blank=True, default="musicDefault.png")
    audio = models.FileField(upload_to="records", default=None)
    isLiked = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    def __str__(self):
        return self.name

class Review(models.Model):
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    def __str__(self):
        return str(self.name)

class Like(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    _id = models.AutoField(primary_key=True, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, default="default.jpg")
    def __str__(self):
        return str(self.user)