from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Place, FavoritePlace, PlaceScore, Token, Relation, FavoritePlaceType, PlaceType
from .serializers import UserSerializer, PlaceSerializer, MenusSerializer, PlaceReviewsSerializer, \
    UserReviewsSerializer, PlaceScoreSerializer, ReviewSerializer, CreateFriendSerializer, \
    UploadPlaceImageSerializer, FavoritePlacesSerializer, PlaceListSerializer, \
    CreateFavoritePlaceSerializer, TokenSerializer, RelationSerializer, FavoritePlaceTypeSerializer, \
    SimpleUserSerializer


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
            data = revision_profile_image(serializer.data, "profile_image")
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            user = get_user(request.data.get('phone_number'))
            serializer = UserSerializer(user)
            data = revision_profile_image(serializer.data, "profile_image")
            return Response(data)

    def put(self, request, format=None):
        user = get_user(request.data.get('phone_number'))
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = revision_profile_image(serializer.data, "profile_image")
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        user = get_user(request.data.get('phone_number'))
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadUserProfile(APIView):
    def post(self, request):
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
    def get(self, request, your_phone_number, user_phone_number, format=None):
        your_user = get_user(your_phone_number)
        user = get_user(user_phone_number)
        serializer = UserSerializer(user)
        is_following = check_relation(your_user, user)
        data = serializer.data.copy()
        data["user_score"] = calculate_user_score(data)
        if data["first_name"] is None:
            data["first_name"] = ""
        if data["last_name"] is None:
            data["last_name"] = ""
        if is_following is None:
            data["is_following"] = 0
        else:
            data["is_following"] = 1
        data = revision_profile_image(data, "profile_image")
        return Response(data)


class PlaceList(APIView):
    """
    Retrieve places.
    """
    def get_total_places(self):
        places = Place.objects.all()
        serializer = PlaceListSerializer(places, many=True)
        data = revision_place_images(serializer.data, "place_image")
        data = sort_total_places(data)
        return data

    def get_suggested_places_by_user(self, user):
        places = []
        favorite_place_types = []
        try:
            for item in FavoritePlaceType.objects.filter(user=user):
                favorite_place_types.append(item)
        except FavoritePlaceType.DoesNotExist:
            favorite_place_types = []
        for favorite_place_type in favorite_place_types:
            for item in PlaceType.objects.filter(type=favorite_place_type):
                places.append(item.place)
        if len(places):
            serializer = PlaceListSerializer(places, many=True)
            data = revision_place_images(serializer.data, "place_image")
            places = []
            for item in data:
                if check_place_list(places, item):
                    places.append(item)
        return places

    def suggested_places_by_relation(self, user, places):
        following_users = []
        serializer = RelationSerializer(user)
        data = serializer.data.copy()
        for following_user in data["followings"]:
            following_users.append(get_user(following_user.get("phone_number")))
        for following_user in following_users:
            places_following_user = self.get_suggested_places_by_user(following_user)
            for place in places_following_user:
                if check_place_list(places, place):
                    places.append(place)

            favorite_places_serializer = FavoritePlacesSerializer(following_user).data.copy()
            favorite_places = []
            for item in favorite_places_serializer["favorite_places"]:
                favorite_places.append(get_place(item["id"]))
            place_serializer = PlaceListSerializer(favorite_places, many=True)
            data = revision_place_images(place_serializer.data, "place_image")
            for place in data:
                if check_place_list(places, place):
                    places.append(place)

        data = sort_total_places(places)
        if len(data) > 30:
            return data[:30]
        return data

    def get(self, request, phone_number):
        user = get_user(phone_number)
        places = self.get_suggested_places_by_user(user)

        return Response({
            "total_places": self.get_total_places(),
            "suggested_places": self.suggested_places_by_relation(user, places)
        })


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
        if score_data["total_score"] is None:
            score_data["total_score"] = 0
        if score_data["food_score"] is None:
            score_data["food_score"] = 0
        if score_data["service_score"] is None:
            score_data["service_score"] = 0
        if score_data["ambiance_score"] is None:
            score_data["ambiance_score"] = 0
        if check_favorite_place(user, place) is None:
            is_favorite = 0
        else:
            is_favorite = 1
        return Response({
            "place": place_serializer.data,
            "place_score": score_data,
            "is_favorite": is_favorite
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
        data = revision_review_profile_images(serializer.data, "profile_image")
        return Response(data)


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
        user = get_user(request.data.get('user'))
        place = get_place(request.data.get('place'))
        data = request.data.copy()
        data["user"] = user.id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRelation(APIView):
    """
    Retrieve friend list.
    """
    def get(self, request, your_phone_number, user_phone_number, format=None):
        user = get_user(user_phone_number)
        your_user = get_user(your_phone_number)
        serializer = RelationSerializer(user)
        data = serializer.data.copy()
        data = revision_relation_profile_images(data, "profile_image")
        for relation_data in data["followers"]:
            if check_relation(your_user, get_user(relation_data["phone_number"])) is None:
                relation_data["is_following"] = 0
            else:
                relation_data["is_following"] = 1
        for relation_data in data["followings"]:
            if check_relation(your_user, get_user(relation_data["phone_number"])) is None:
                relation_data["is_following"] = 0
            else:
                relation_data["is_following"] = 1
        return Response(data)


class EditRelation(APIView):
    """
    Follow and Unfollow another user.
    """
    def post(self, request):
        follower_user = get_user(request.data.get("follower"))
        following_user = get_user(request.data.get("following"))
        friend = check_relation(follower_user, following_user)
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
        friend = get_relation(request.data.get('follower'), request.data.get('following'))
        friend.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UploadPlaceImage(APIView):
    """
    Upload Place Image.
    """
    def post(self, request):
        user = get_user(request.data.get('user'))
        data = request.data.copy()
        data['user'] = user.id
        data['place'] = int(request.data.get('place'))
        serializer = UploadPlaceImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFavoritePlace(APIView):
    """
    Retrieve Favorite Places of User.
    """
    def get(self, request, phone_number, format=None):
        user = get_user(phone_number)

        serializer = FavoritePlacesSerializer(user)
        data = revision_favorite_places_place_image(serializer.data, "place_image")
        return Response(data)


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
            serializer = CreateFavoritePlaceSerializer(data=data)
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


class EditFavoritePlaceType(APIView):
    """
    Create or Delete Favorite Place Type of User.
    """
    def post(self, request):
        user = get_user(request.data.get("user"))
        favorite_place_type = check_favorite_place_type(user, request.data.get("type"))
        if favorite_place_type is None:
            data = request.data.copy()
            data["user"] = user.id
            serializer = FavoritePlaceTypeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = FavoritePlaceTypeSerializer(favorite_place_type)
            return Response(serializer.data)

    def delete(self, request, format=None):
        favorite_place_type = get_favorite_place_type(request.data.get('user'), request.data.get('type'))
        favorite_place_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Search(APIView):
    """
    Search place & user by name
    """
    def get_places(self, text):
        places = []
        for place in Place.objects.filter(name__contains=text):
            places.append(place)
        place_serializer = PlaceListSerializer(places, many=True)
        data = revision_place_images(place_serializer.data, "place_image")
        places = sort_total_places(data)
        return places

    def get_users(self, text):
        users = []
        for user in User.objects.filter(first_name__contains=text):
            if check_user_list(users, user):
                users.append(user)
        for user in User.objects.filter(last_name__contains=text):
            if check_user_list(users, user):
                users.append(user)
        user_serializer = SimpleUserSerializer(users, many=True)
        return user_serializer.data

    def get(self, request, text):
        return Response({
            "places": self.get_places(text),
            "users": self.get_users(text)
        })


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
    

def get_relation(follower_phone_number, following_phone_number):
    try:
        return Relation.objects.get(follower=get_user(follower_phone_number),
                                    following=get_user(following_phone_number))
    except Relation.DoesNotExist:
        raise Http404


def check_relation(follower_user, following_user):
    try:
        return Relation.objects.get(follower=follower_user, following=following_user)
    except Relation.DoesNotExist:
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


def get_favorite_place_type(user_phone_number, place_type):
    try:
        return FavoritePlaceType.objects.get(user=get_user(user_phone_number), type=place_type)
    except FavoritePlaceType.DoesNotExist:
        raise Http404


def check_favorite_place_type(user, place_type):
    try:
        return FavoritePlaceType.objects.get(user=user, type=place_type)
    except FavoritePlaceType.DoesNotExist:
        return None


def revision_profile_image(data, key):
    data = data.copy()
    if "media" not in data[key]:
        data[key] = "media/" + data[key]
    return data


def revision_place_images(data, key):
    data = data.copy()
    for item in data:
        if "media" not in item[key]:
            item[key] = "media/" + item[key]
    return data


def revision_review_profile_images(data, key):
    data = data.copy()
    for item in data["reviews"]:
        if "media" not in item[key]:
            item[key] = "media/" + item[key]
    return data


def revision_relation_profile_images(data, key):
    data = data.copy()
    for item in data["followers"]:
        if "media" not in item[key]:
            item[key] = "media/" + item[key]
    for item in data["followings"]:
        if "media" not in item[key]:
            item[key] = "media/" + item[key]
    return data


def revision_favorite_places_place_image(data, key):
    data = data.copy()
    for item in data["favorite_places"]:
        if "media" not in item[key]:
            item[key] = "media/" + item[key]
    return data


def calculate_user_score(data):
    user_score = 0
    user_score += (data["followers_count"] * 2)
    user_score += (data["followings_count"] * 1)
    user_score += (data["reviews_count"] * 3)
    user_score += (data["place_scores_count"] * 2)
    user_score += (data["uploaded_images_count"] * 5)
    user_score += (data["favorite_places_count"] * 1)
    return user_score


def sort_total_places(data):
    data_list = []
    for item in data:
        data_list.append(((item["overall_score"] * item["all_scores_count"]), item))
    data_list.sort(key=lambda x: x[0], reverse=True)
    sorted_data = []
    for item in data_list:
        sorted_data.append(item[1])
    return sorted_data


def check_place_list(places, place):
    for p in places:
        if p["id"] == place["id"]:
            return False
    return True


def check_user_list(users, user):
    for u in users:
        if u.phone_number == user.phone_number:
            return False
    return True
