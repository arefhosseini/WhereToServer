from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Place, FavoritePlace, PlaceScore, Friend, Token
from .serializers import UserSerializer, PlaceSerializer, MenusSerializer, PlaceReviewsSerializer, \
    UserReviewsSerializer, PlaceScoreSerializer, ReviewSerializer, FriendSerializer, CreateFriendSerializer, \
    CreatePlaceImageSerializer, FavoritePlacesSerializer, \
    PlaceListSerializer, CreateFavoritePlaceSerializer, TokenSerializer


class Verify(APIView):
    """
    Verify phone number with token
    """
    def post(self, request):
        verify_code = get_verify_code(request.data.get('phone_number'))
        token = get_token(request.data.get('phone_number'))
        data = request.data.copy()
        data["verify_code"] = verify_code
        if token is None:
            serializer = TokenSerializer(data=data)
        else:
            serializer = TokenSerializer(token, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    """
    Create, Edit, Delete User
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            user = get_user(request.data.get('phone_number'))
            serializer = UserSerializer(user)
            return Response(serializer.data)

    def put(self, request, format=None):
        user = get_user(request.data.get('phone_number'))
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = get_user(request.data.get('phone_number'))
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadUserProfile(APIView):
    def post(self, request):
        print(request.data)
        user = get_user(request.data.get('phone_number'))
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "ok"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve user.
    """
    def get(self, request, phone_number, format=None):
        user = get_user(phone_number)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class PlaceList(APIView):
    """
    Retrieve places.
    """
    def get(self, request, phone_number):
        user = get_user(phone_number)

        places = Place.objects.all()
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)


class PlaceDetail(APIView):
    """
    Retrieve place.
    """
    def get(self, request, phone_number, pk, format=None):
        user = get_user(phone_number)
        place = get_place(pk)
        place_score = check_place_score(user, place)
        place_serializer = PlaceSerializer(place)
        score_data = PlaceScoreSerializer(place_score).data.copy()
        score_data["user"] = user.phone_number
        return Response({
            "place": place_serializer.data,
            "place_score": score_data
        })


class MenuDetail(APIView):
    """
    Retrieve menu of place.
    """
    def get(self, request, pk, format=None):
        place = get_place(pk)

        serializer = MenusSerializer(place)
        return Response(serializer.data)


class PlaceReviewDetail(APIView):
    """
    Retrieve reviews of place.
    """
    def get(self, request, pk, format=None):
        place = get_place(pk)

        serializer = PlaceReviewsSerializer(place)
        serializer.data["reviews"].reverse()
        return Response(serializer.data)


class UserReviewDetail(APIView):
    """
    Retrieve reviews of user.
    """
    def get(self, request, phone_number, format=None):
        user = get_user(phone_number)

        serializer = UserReviewsSerializer(user)
        return Response(serializer.data)


class ScoreDetail(APIView):
    """
    Create new score.
    """
    def post(self, request):
        user = get_user(request.data.get('user'))
        place = get_place(request.data.get('place'))
        place_score = check_place_score(user, place)
        data = request.data.copy()
        data["user"] = user.id
        if place_score is None:
            serializer = PlaceScoreSerializer(data=data)
        else:
            serializer = PlaceScoreSerializer(place_score, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        place_score = get_place_score(request.data.get('user'))

        serializer = PlaceScoreSerializer(place_score, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    """
    Create new review.
    """
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFriend(APIView):
    """
    Retrieve friend list.
    """
    def get(self, request, phone_number, format=None):
        user = get_user(phone_number)

        serializer = FriendSerializer(user)
        return Response(serializer.data)


class EditFriend(APIView):
    """
    Follow and Unfollow another user.
    """
    def post(self, request):
        follower_user = get_user(request.data.get("follower"))
        following_user = get_user(request.data.get("following"))
        friend = check_friend(follower_user, following_user)
        if friend is None:
            data = request.data.copy()
            data["follower"] = follower_user.id
            data["following"] = following_user.id
            serializer = CreateFriendSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CreateFriendSerializer(friend)
            return Response(serializer.data)

    def delete(self, request, format=None):
        friend = get_friend(request.data.get('follower'), request.data.get('following'))
        friend.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatePlaceImage(APIView):
    """
    Upload Place Image.
    """
    def post(self, request):
        serializer = CreatePlaceImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFavoritePlace(APIView):
    """
    Retrieve Favorite Places of User.
    """
    def get(self, request, phone_number, format=None):
        user = get_user(phone_number)

        serializer = FavoritePlacesSerializer(user)
        return Response(serializer.data)


class EditFavoritePlace(APIView):
    """
    Create or Delete Favorite Place of User.
    """
    def post(self, request):
        user = get_user(request.data.get("user"))
        place = get_place(request.data.get("place"))
        favorite_place = check_favorite_place(user, place)
        if favorite_place is None:
            data = request.data.copy()
            data["user"] = user.id
            serializer = CreateFavoritePlaceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CreateFavoritePlaceSerializer(favorite_place)
            return Response(serializer.data)

    def delete(self, request, format=None):
        favorite_place = get_favorite_place(request.data.get('user'), request.data.get('place'))
        favorite_place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def get_verify_code(phone_number):
    return "55555"


def get_token(phone_number):
    try:
        return Token.objects.get(phone_number=phone_number)
    except Token.DoesNotExist:
        return None


def get_user(phone_number):
    try:
        return User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        raise Http404
    

def get_place(pk):
    try:
        return Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        raise Http404


def get_place_score(pk):
    try:
        return PlaceScore.objects.get(pk=pk)
    except PlaceScore.DoesNotExist:
        raise Http404


def check_place_score(user, place):
    try:
        return PlaceScore.objects.get(user=user, place=place)
    except PlaceScore.DoesNotExist:
        return None
    

def get_friend(follower_phone_number, following_phone_number):
    try:
        return Friend.objects.get(follower=get_user(follower_phone_number), following=get_user(following_phone_number))
    except Friend.DoesNotExist:
        raise Http404


def check_friend(follower_user, following_user):
    try:
        return Friend.objects.get(follower=follower_user, following=following_user)
    except Friend.DoesNotExist:
        return None


def get_favorite_place(user_phone_number, place_id):
    try:
        return FavoritePlace.objects.get(user=get_user(user_phone_number), place=get_place(place_id))
    except FavoritePlace.DoesNotExist:
        raise Http404


def check_favorite_place(user, place):
    try:
        return FavoritePlace.objects.get(user=user, place=place)
    except FavoritePlace.DoesNotExist:
        return None
