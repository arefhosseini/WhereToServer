from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import User, Place
from .serializers import UserSerializer, PlaceSerializer, MenusSerializer, PlaceReviewsSerializer, \
    UserReviewsSerializer, ScoreSerializer, ReviewSerializer, FriendSerializer, CreateFriendSerializer


class UserList(APIView):
    """
    List all Users, or create a new user.
    """
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

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class PlaceReview(APIView):
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


class UserReview(APIView):
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


class Score(APIView):
    """
    Create a new score.
    """
    def post(self, request):
        serializer = ScoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Review(APIView):
    """
    Create a new review.
    """
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Friend(APIView):
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


class CreateFriend(APIView):
    """
    Follow another user.
    """
    def post(self, request):
        serializer = CreateFriendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
