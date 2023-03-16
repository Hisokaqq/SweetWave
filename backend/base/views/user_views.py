from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.serializers import  UserSerializer, UserSerializerWithToken
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import status
from base.models import Song, Like, Profile

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v
        
        return data
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(["POST"])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name=data["name"],
            username=data["email"],
            email=data["email"],
            password=make_password(data["password"])
        )
    except:
        message = {"detail":"User with this email already exists"}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addAvatar(request):
    user = request.user
    data = request.data
    profile = Profile.objects.get(user = user)
    print(data)
    profile.avatar = request.FILES.get("avatar")
    profile.save()
    print("success")
    # profile.avatar = ["avatar"]
    # profile.save()
    return Response("avatar changed")



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([ IsAdminUser])
def getUsers(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])      
def addLike(request, pk):
    user = request.user
    song = Song.objects.get(_id = pk)
    alreadyExists = song.like_set.filter(user=user).exists()
    if not alreadyExists:
        like = Like.objects.create(
            user=user,
            song=song,
        )
        like.save()
        return Response("like added")
    else:
        # print("asdas as das dasd asd asd as dasds das das da sdasd asd s3s dasd asd asd as dasds das das da sdasd asd s3s dasd asd asd as dasds das das da sdasd asd s3s dasd asd asd as dasds das das da sdasd asd s3s dasd asd asd as dasds das das da sdasd asd s3")
        song.like_set.get(user=user).delete()
        content = {"details": "like is deleted"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


    
    
    

    