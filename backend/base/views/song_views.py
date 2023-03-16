from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.models import Song, Review
from base.serializers import SongSerializer
from rest_framework import status

@api_view(["GET"])
def getSongs(request):
    songs = Song.objects.all()
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getSong(request, pk):
    song = Song.objects.get(_id = pk)
    serializer = SongSerializer(song, many=False)
    return Response(serializer.data)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createSongReview(request, pk):
    user = request.user
    song = Song.objects.get(_id = pk)
    data = request.data
    alreadyExists = song.review_set.filter(user=user).exists()
    if alreadyExists:
        
        content = {"details": "Song has been already reviewed"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif data["rating"] == 0:
        content = {"details": "Rating cant be 0"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        review = Review.objects.create(
            user=user,
            song=song,
            name=user.first_name,
            rating = data["rating"],
            comment = data["comment"],
        )
        reviews = song.review_set.all()
        song.numReviews = len(reviews)
        
        total = 0
        for i in reviews:
            total += i.rating
        song.rating = total / len(reviews)
        song.save()
        review.save()
        return Response("Review Added")
        
        

    