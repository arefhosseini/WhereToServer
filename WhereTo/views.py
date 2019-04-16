from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import User, Place, FavoritePlace, PlaceScore, Review, Friend
from .serializers import UserSerializer, PlaceSerializer, MenusSerializer, PlaceReviewsSerializer, \
    UserReviewsSerializer, ScoreSerializer, ReviewSerializer, FriendSerializer, CreateFriendSerializer, \
    CreatePlaceImageSerializer, FavoritePlaceSerializer, CreateFavoritePlace, FavoritePlacesSerializer, \
    PlaceListSerializer


class UserList(APIView):
    """
    List all Users, or create a new user.
    """
    def get_object(self, phone_number):
        try:
            return User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise Http404

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        user = self.get_object(request.data.get('phone_number'))
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = self.get_object(request.data.get('phone_number'))
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, phone_number):
        try:
            return User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, phone_number, format=None):
        user = self.get_object(phone_number)

        serializer = UserSerializer(user)
        return Response(serializer.data)


class PlaceList(APIView):
    """
    Retrieve places.
    """
    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceListSerializer(places, many=True)
        return Response(serializer.data)


class PlaceDetail(APIView):
    """
    Retrieve a place instance.
    """
    def get_object(self, pk):
        try:
            return Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        place = self.get_object(pk)

        serializer = PlaceSerializer(place)
        return Response(serializer.data)


class MenuDetail(APIView):
    """
    Retrieve a menu instance.
    """
    def get_object(self, pk):
        try:
            return Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        place = self.get_object(pk)

        serializer = MenusSerializer(place)
        return Response(serializer.data)


class PlaceReviewDetail(APIView):
    """
    Retrieve a menu instance.
    """
    def get_object(self, pk):
        try:
            return Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        place = self.get_object(pk)

        serializer = PlaceReviewsSerializer(place)
        return Response(serializer.data)


class UserReviewDetail(APIView):
    """
    Retrieve a menu instance.
    """
    def get_object(self, phone_number):
        try:
            return User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, phone_number, format=None):
        user = self.get_object(phone_number)

        serializer = UserReviewsSerializer(user)
        return Response(serializer.data)


class ScoreDetail(APIView):
    """
    Create a new score.
    """
    def get_object(self, pk):
        try:
            return PlaceScore.objects.get(pk=pk)
        except PlaceScore.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        user = self.get_object(request.data.get('user'))
        serializer = ScoreSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    """
    Create a new review.
    """
    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        user = self.get_object(request.data.get('user'))
        serializer = ReviewSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFriend(APIView):
    """
    Follow another user.
    """
    def get_object(self, phone_number):
        try:
            return User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, phone_number, format=None):
        user = self.get_object(phone_number)

        serializer = FriendSerializer(user)
        return Response(serializer.data)


class EditFriend(APIView):
    """
    Follow and Unfollow another user.
    """
    def get_object(self, follower, following):
        try:
            return Friend.objects.get(follower=User.objects.get(phone_number=follower),
                                      following=User.objects.get(phone_number=following))
        except User.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = CreateFriendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        favorite_place = self.get_object(request.data.get('follower'), request.data.get('following'))
        favorite_place.delete()
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
    Get Favorite Place of User.
    """
    def get_object(self, phone_number):
        try:
            return User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, phone_number, format=None):
        user = self.get_object(phone_number)

        serializer = FavoritePlacesSerializer(user)
        return Response(serializer.data)


class EditFavoritePlace(APIView):
    """
    Follow another user.
    """
    def get_object(self, user, place):
        try:
            return FavoritePlace.objects.get(user=user, place=place)
        except FavoritePlace.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = CreateFavoritePlace(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        favorite_place = self.get_object(request.data.get('user'), request.data.get('place'))
        favorite_place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
