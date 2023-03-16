from django.urls import path
from base.views import song_views as views

urlpatterns = [

    path("", views.getSongs, name="songs"),
    path("<str:pk>/", views.getSong, name="song"),
    path("<str:pk>/reviews/", views.createSongReview, name="create-review"),
] 