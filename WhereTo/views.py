from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Place, FavoritePlace, PlaceScore, Token, Relation, FavoritePlaceType, PlaceType, ReviewVote, \
    Review, PlaceImage, PlaceImageVote
from .serializers import UserSerializer, PlaceSerializer, MenusSerializer, PlaceReviewsSerializer, \
    UserReviewsSerializer, PlaceScoreSerializer, ReviewSerializer, CreateFriendSerializer, \
    UploadPlaceImageSerializer, FavoritePlacesSerializer, PlaceListSerializer, \
    CreateFavoritePlaceSerializer, TokenSerializer, RelationSerializer, FavoritePlaceTypeSerializer, \
    SimpleUserSerializer, ReviewVoteSerializer, PlaceImageVoteSerializer, HashtagSerializer, UserScoresSerializer, \
    UserPlaceImagesSerializer, UserControlSerializer


class VerifyUser(APIView):
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


class UserControl(APIView):
    """
    Create, Edit, Delete User
    """
    def post(self, request):
        serializer = UserControlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            user = get_user(request.data.get('phone_number'))
            serializer = UserControlSerializer(user)
            return Response(serializer.data)

    def put(self, request, format=None):
        user = get_user(request.data.get('phone_number'))
        serializer = UserControlSerializer(user, data=request.data)
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
        data = serializer.data.copy()
        data["user_score"] = calculate_user_score(data)
        if data["first_name"] is None:
            data["first_name"] = ""
        if data["last_name"] is None:
            data["last_name"] = ""

        is_following = check_relation(your_user, user)
        if is_following is None:
            data["is_following"] = 0
        else:
            data["is_following"] = 1
        return Response(data)


class PlaceList(APIView):
    """
    Retrieve places.
    """
    def get_total_places(self):
        places = Place.objects.all()
        serializer = PlaceListSerializer(places, many=True)
        data = sort_total_places(serializer.data)
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
            places = []
            for item in serializer.data:
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
            for place in place_serializer.data.copy():
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
        place_data = place_serializer.data.copy()
        for place_image in place_data["place_images"]:
            place_image_vote = check_place_image_vote(user, get_place_image(place_image["id"]))
            if place_image_vote is None:
                place_image["your_vote"] = 0
            elif place_image_vote.vote == 1:
                place_image["your_vote"] = 1
            else:
                place_image["your_vote"] = -1
        return Response({
            "place": place_data,
            "place_score": score_data,
            "is_favorite": is_favorite
        })


class MenuList(APIView):
    """
    Retrieve menu of place.
    """
    def get(self, request, phone_number, pk, format=None):
        place = get_place(pk)

        serializer = MenusSerializer(place)
        return Response(serializer.data)


class PlaceReviewList(APIView):
    """
    Retrieve reviews of place.
    """
    def get(self, request, phone_number, pk, format=None):
        place = get_place(pk)
        your_user = get_user(phone_number)
        serializer = PlaceReviewsSerializer(place)
        serializer.data["reviews"].reverse()
        data = serializer.data.copy()
        for review in data["reviews"]:
            place_score = check_place_score(get_user(review["phone_number"]), place)
            if place_score is not None:
                review["place_score"] = place_score.total_score
            else:
                review["place_score"] = 0
            review_vote = check_review_vote(your_user, get_review(review["id"]))
            if review_vote is None:
                review["your_vote"] = 0
            elif review_vote.vote == 1:
                review["your_vote"] = 1
            else:
                review["your_vote"] = -1
        return Response(data)


class UserReviewList(APIView):
    """
    Retrieve reviews of user.
    """
    def get(self, request, your_phone_number, user_phone_number, format=None):
        user = get_user(user_phone_number)
        your_user = get_user(your_phone_number)
        data = UserReviewsSerializer(user).data.copy()
        data["reviews"].reverse()
        for review in data["reviews"]:
            place_score = check_place_score(user, get_place(review["place_id"]))
            if place_score is not None:
                review["place_score"] = place_score.total_score
            else:
                review["place_score"] = 0
            review_vote = check_review_vote(your_user, get_review(review["id"]))
            if review_vote is None:
                review["your_vote"] = 0
            elif review_vote.vote == 1:
                review["your_vote"] = 1
            else:
                review["your_vote"] = -1
        return Response(data)


class UserPlaceScoreList(APIView):
    """
    Retrieve place scores of user.
    """
    def get(self, request, your_phone_number, user_phone_number, format=None):
        user = get_user(user_phone_number)
        serializer = UserScoresSerializer(user)
        return Response(serializer.data)


class UserImageList(APIView):
    """
    Retrieve scores of user.
    """
    def get(self, request, your_phone_number, user_phone_number, format=None):
        user = get_user(user_phone_number)
        your_user = get_user(your_phone_number)
        data = UserPlaceImagesSerializer(user).data.copy()
        for place_image in data["place_images"]:
            place_image_vote = check_place_image_vote(your_user, get_place_image(place_image["id"]))
            if place_image_vote is None:
                place_image["your_vote"] = 0
            elif place_image_vote.vote == 1:
                place_image["your_vote"] = 1
            else:
                place_image["your_vote"] = -1
        return Response(data)


class ScoreControl(APIView):
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
            return Response({"status": "ok"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        place_score = get_place_score(request.data.get('user'))

        serializer = PlaceScoreSerializer(place_score, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewControl(APIView):
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
            hashtags = get_hashtags(serializer.data.get("text"))
            hashtag_data = {
                "place": place.id,
                "review": serializer.data.get("id")
            }
            for hashtag in hashtags:
                hashtag_data["name"] = hashtag
                hashtag_serializer = HashtagSerializer(data=hashtag_data)
                if hashtag_serializer.is_valid():
                    hashtag_serializer.save()
            return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RelationList(APIView):
    """
    Retrieve friend list.
    """
    def get(self, request, your_phone_number, user_phone_number, format=None):
        user = get_user(user_phone_number)
        your_user = get_user(your_phone_number)
        serializer = RelationSerializer(user)
        data = serializer.data.copy()
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


class RelationControl(APIView):
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
                return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CreateFriendSerializer(friend)
            return Response({"status": "ok"})

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


class FavoritePlaceList(APIView):
    """
    Retrieve Favorite Places of User.
    """
    def get(self, request, your_phone_number, user_phone_number, format=None):
        user = get_user(user_phone_number)
        your_user = get_user(your_phone_number)
        serializer = FavoritePlacesSerializer(user)
        data = serializer.data.copy()
        for item in data["favorite_places"]:
            favorite_place = check_favorite_place(your_user, get_place(item["id"]))
            if favorite_place is None:
                item["is_your_favorite"] = 0
            else:
                item["is_your_favorite"] = 1
        return Response(data)


class FavoritePlaceControl(APIView):
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
                return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CreateFavoritePlaceSerializer(favorite_place)
            return Response({"status": "ok"})

    def delete(self, request, format=None):
        favorite_place = get_favorite_place(request.data.get('user'), request.data.get('place'))
        favorite_place.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoritePlaceTypeControl(APIView):
    """
    Create or Delete Favorite Place Type of User.
    """
    def post(self, request):
        user = get_user(request.data.get("user"))
        data = {"user": user.id}
        for place_type in request.data.get("add_types"):
            favorite_place_type = check_favorite_place_type(user, place_type)
            if favorite_place_type is None:
                data["type"] = place_type
                serializer = FavoritePlaceTypeSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        for place_type in request.data.get("delete_types"):
            favorite_place_type = get_favorite_place_type(request.data.get('user'), place_type)
            favorite_place_type.delete()
        return Response({"status": "ok"})


class SearchPlace(APIView):
    """
    Search place by name
    """
    def get(self, request, text):
        places = []
        phrases = text.split()
        phrases.append(text)
        for phrase in phrases:
            for place in Place.objects.filter(name__contains=phrase):
                if check_place_list_object(places, place):
                    places.append(place)
        place_serializer = PlaceListSerializer(places, many=True)
        places = sort_total_places(place_serializer.data)
        return Response(places)


class SearchUser(APIView):
    """
    Search user by name
    """
    def get(self, request, text):
        users = []
        phrases = text.split()
        if text not in phrases:
            phrases.append(text)
        for phrase in phrases:
            for user in User.objects.filter(first_name__contains=phrase):
                if check_user_list(users, user):
                    users.append(user)
            for user in User.objects.filter(last_name__contains=phrase):
                if check_user_list(users, user):
                    users.append(user)
        user_serializer = SimpleUserSerializer(users, many=True)
        return Response(user_serializer.data)


class ReviewVoteControl(APIView):
    """
    Create or Delete Review Vote.
    """
    def post(self, request):
        user = get_user(request.data.get("user"))
        review = get_review(request.data.get("review"))
        review_vote = check_review_vote(user, review)
        if review_vote is None:
            data = request.data.copy()
            data["user"] = user.id
            serializer = ReviewVoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            review_vote.vote = request.data.get("vote")
            review_vote.save()
            return Response({"status": "ok"})

    def delete(self, request, format=None):
        review_vote = get_review_vote(request.data.get('user'), request.data.get('review'))
        review_vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlaceImageVoteControl(APIView):
    """
    Create or Delete Place Image Vote.
    """
    def post(self, request):
        user = get_user(request.data.get("user"))
        place_image = get_place_image(request.data.get("place_image"))
        place_image_vote = check_place_image_vote(user, place_image)
        if place_image_vote is None:
            data = request.data.copy()
            data["user"] = user.id
            serializer = PlaceImageVoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            place_image_vote.vote = request.data.get("vote")
            place_image_vote.save()
            return Response({"status": "ok"})

    def delete(self, request, format=None):
        place_image_vote = get_place_image_vote(request.data.get('user'), request.data.get('place_image'))
        place_image_vote.delete()
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


def get_relation(follower_phone_number, following_phone_number):
    try:
        return Relation.objects.get(follower=get_user(follower_phone_number),
                                    following=get_user(following_phone_number))
    except Relation.DoesNotExist:
        raise Http404


def get_review(pk):
    try:
        return Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        raise Http404


def get_place_image(pk):
    try:
        return PlaceImage.objects.get(pk=pk)
    except PlaceImage.DoesNotExist:
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


def get_review_vote(user_phone_number, review_id):
    try:
        return ReviewVote.objects.get(user=get_user(user_phone_number), review=get_review(review_id))
    except ReviewVote.DoesNotExist:
        raise Http404


def check_review_vote(user, review):
    try:
        return ReviewVote.objects.get(user=user, review=review)
    except ReviewVote.DoesNotExist:
        return None


def get_place_image_vote(user_phone_number, place_image_id):
    try:
        return PlaceImageVote.objects.get(user=get_user(user_phone_number), place_image=get_place_image(place_image_id))
    except PlaceImageVote.DoesNotExist:
        raise Http404


def check_place_image_vote(user, place_image):
    try:
        return PlaceImageVote.objects.get(user=user, place_image=place_image)
    except PlaceImageVote.DoesNotExist:
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


def check_place_list_object(places, place):
    for p in places:
        if p.id == place.id:
            return False
    return True


def check_user_list(users, user):
    for u in users:
        if u.phone_number == user.phone_number:
            return False
    return True


def get_hashtags(text):
    hashtags = []
    phrases = text.split()
    for phrase in phrases:
        if phrase[0] == "#":
            hashtags.append(phrase)
    return hashtags
