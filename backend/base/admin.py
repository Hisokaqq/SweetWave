from django.contrib import admin
from .models import Song, Review, Like, Profile

admin.site.register(Song)
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(Profile)
