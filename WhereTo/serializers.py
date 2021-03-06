from rest_framework import serializers

from WhereToServer import settings
from .models import User, Place, PlaceImage, CoordinatePlace, Menu, Food, Review, PlaceScore, Relation, FavoritePlace, \
    Token, FavoritePlaceType, ReviewVote, PlaceImageVote, Hashtag


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('phone_number', 'verify_code')


class FavoritePlaceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoritePlaceType
        fields = ('user', 'type')


class UserControlSerializer(serializers.ModelSerializer):
    favorite_place_types = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='type'
    )

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'profile_image', 'first_name', 'last_name', 'favorite_place_types')


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    place_scores_count = serializers.SerializerMethodField()
    uploaded_images_count = serializers.SerializerMethodField()
    favorite_places_count = serializers.SerializerMethodField()
    favorite_place_types = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='type'
    )

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'profile_image', 'first_name', 'last_name', 'user_score',
                  'followers_count', 'followings_count', 'reviews_count', 'place_scores_count',
                  'uploaded_images_count', 'favorite_places_count', 'favorite_place_types')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()

    def get_place_scores_count(self, obj):
        return obj.place_scores.count()

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def get_uploaded_images_count(self, obj):
        return obj.place_images.count()

    def get_favorite_places_count(self, obj):
        return obj.favorite_places.count()


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number', 'profile_image', 'first_name', 'last_name')


class PlaceListSerializer(serializers.ModelSerializer):
    place_types = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='type'
    )
    overall_score = serializers.SerializerMethodField()
    all_scores_count = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ('id', 'name', 'place_types', 'place_image', 'overall_score', 'all_scores_count')

    def get_overall_score(self, obj):
        all_scores = obj.place_scores.all()
        average = 0
        for score in all_scores:
            average += score.total_score
        if len(all_scores) > 0:
            return average / len(all_scores)
        return 0

    def get_all_scores_count(self, obj):
        return obj.place_scores.count()


class PlaceImageSerializer(serializers.ModelSerializer):
    up_votes = serializers.SerializerMethodField()
    down_votes = serializers.SerializerMethodField()

    class Meta:
        model = PlaceImage
        fields = ('id', 'user', 'place', 'up_votes', 'down_votes', 'image')

    def get_up_votes(self, obj):
        return obj.place_image_votes.filter(vote=1).count()

    def get_down_votes(self, obj):
        return obj.place_image_votes.filter(vote=-1).count()


class CoordinatePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordinatePlace
        fields = ('latitude', 'longitude')


class PlaceScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaceScore
        fields = ('id', 'user', 'place', 'total_score', 'food_score', 'service_score', 'ambiance_score')


class PlaceSerializer(serializers.ModelSerializer):
    place_types = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='type'
     )
    place_images = PlaceImageSerializer(many=True)
    overall_score = serializers.SerializerMethodField()
    all_scores_count = serializers.SerializerMethodField()
    one_score_count = serializers.SerializerMethodField()
    two_score_count = serializers.SerializerMethodField()
    three_score_count = serializers.SerializerMethodField()
    four_score_count = serializers.SerializerMethodField()
    five_score_count = serializers.SerializerMethodField()
    food_score_average = serializers.SerializerMethodField()
    service_score_average = serializers.SerializerMethodField()
    ambiance_score_average = serializers.SerializerMethodField()
    coordinate_place = CoordinatePlaceSerializer(many=True)
    phones_place = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='phone_number'
    )

    class Meta:
        model = Place
        fields = ('id', 'name', 'price_degree', 'address', 'open_hours', 'price', 'features',
                  'state', 'city', 'place_image', 'place_types', 'place_images', 'overall_score',
                  'all_scores_count', 'one_score_count', 'two_score_count', 'three_score_count',
                  'four_score_count', 'five_score_count', 'food_score_average', 'service_score_average',
                  'ambiance_score_average', 'coordinate_place', 'phones_place')

    def get_overall_score(self, obj):
        all_scores = obj.place_scores.all()
        average = 0
        for score in all_scores:
            average += score.total_score
        if len(all_scores) > 0:
            return round((average / len(all_scores)), 1)
        return 0

    def get_all_scores_count(self, obj):
        return obj.place_scores.count()

    def get_one_score_count(self, obj):
        all_scores = obj.place_scores.all()
        count = 0
        for score in all_scores:
            if score.total_score == 1:
                count += score.total_score
        return count

    def get_two_score_count(self, obj):
        all_scores = obj.place_scores.all()
        count = 0
        for score in all_scores:
            if score.total_score == 2:
                count += 1
        return count

    def get_three_score_count(self, obj):
        all_scores = obj.place_scores.all()
        count = 0
        for score in all_scores:
            if score.total_score == 3:
                count += 1
        return count

    def get_four_score_count(self, obj):
        all_scores = obj.place_scores.all()
        count = 0
        for score in all_scores:
            if score.total_score == 4:
                count += 1
        return count

    def get_five_score_count(self, obj):
        all_scores = obj.place_scores.all()
        count = 0
        for score in all_scores:
            if score.total_score == 5:
                count += 1
        return count

    def get_food_score_average(self, obj):
        all_scores = obj.place_scores.all()
        average = 0
        for score in all_scores:
            average += score.food_score
        if len(all_scores) > 0:

            return round((average / len(all_scores)), 1)
        return 0

    def get_service_score_average(self, obj):
        all_scores = obj.place_scores.all()
        average = 0
        for score in all_scores:
            average += score.service_score
        if len(all_scores) > 0:
            return round((average / len(all_scores)), 1)
        return 0

    def get_ambiance_score_average(self, obj):
        all_scores = obj.place_scores.all()
        average = 0
        for score in all_scores:
            average += score.ambiance_score
        if len(all_scores) > 0:
            return round((average / len(all_scores)), 1)
        return 0


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('name', 'detail', 'price')


class MenuSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(many=True)

    class Meta:
        model = Menu
        fields = ('name', 'foods')


class MenusSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True)

    class Meta:
        model = Place
        fields = ('id', 'menus')


class PlaceReviewSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    up_votes = serializers.SerializerMethodField()
    down_votes = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'profile_image',
                  'text', 'created_date', 'up_votes', 'down_votes')

    def get_phone_number(self, obj):
        return obj.user.phone_number

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_profile_image(self, obj):
        return settings.MEDIA_URL + obj.user.profile_image.name

    def get_created_date(self, obj):
        return round(obj.created_date.timestamp() * 1000)

    def get_up_votes(self, obj):
        return obj.review_votes.filter(vote=1).count()

    def get_down_votes(self, obj):
        return obj.review_votes.filter(vote=-1).count()


class PlaceReviewsSerializer(serializers.ModelSerializer):
    reviews = PlaceReviewSerializer(many=True)

    class Meta:
        model = Place
        fields = ('id', 'reviews')


class UserReviewSerializer(serializers.ModelSerializer):
    place_id = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()
    place_image = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    up_votes = serializers.SerializerMethodField()
    down_votes = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'created_date',
                  'up_votes', 'down_votes', 'place_id', 'place_name', 'place_image')

    def get_place_id(self, obj):
        return obj.place.id

    def get_place_name(self, obj):
        return obj.place.name

    def get_place_image(self, obj):
        return settings.MEDIA_URL + obj.place.place_image.name

    def get_created_date(self, obj):
        return round(obj.created_date.timestamp() * 1000)

    def get_up_votes(self, obj):
        return obj.review_votes.filter(vote=1).count()

    def get_down_votes(self, obj):
        return obj.review_votes.filter(vote=-1).count()


class UserReviewsSerializer(serializers.ModelSerializer):
    reviews = UserReviewSerializer(many=True)

    class Meta:
        model = User
        fields = ('phone_number', 'reviews')


class UserScoreSerializer(serializers.ModelSerializer):
    place_id = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()
    place_image = serializers.SerializerMethodField()

    class Meta:
        model = PlaceScore
        fields = ('total_score', 'food_score', 'service_score', 'ambiance_score',
                  'place_id', 'place_name', 'place_image')

    def get_place_id(self, obj):
        return obj.place.id

    def get_place_name(self, obj):
        return obj.place.name

    def get_place_image(self, obj):
        return settings.MEDIA_URL + obj.place.place_image.name


class UserScoresSerializer(serializers.ModelSerializer):
    place_scores = UserScoreSerializer(many=True)

    class Meta:
        model = User
        fields = ('phone_number', 'place_scores')


class UserPlaceImageSerializer(serializers.ModelSerializer):
    place_id = serializers.SerializerMethodField()
    place_name = serializers.SerializerMethodField()
    up_votes = serializers.SerializerMethodField()
    down_votes = serializers.SerializerMethodField()

    class Meta:
        model = PlaceImage
        fields = ('id', 'image', 'place_id', 'place_name', 'up_votes', 'down_votes')

    def get_place_id(self, obj):
        return obj.place.id

    def get_place_name(self, obj):
        return obj.place.name

    def get_up_votes(self, obj):
        return obj.place_image_votes.filter(vote=1).count()

    def get_down_votes(self, obj):
        return obj.place_image_votes.filter(vote=-1).count()


class UserPlaceImagesSerializer(serializers.ModelSerializer):
    place_images = UserPlaceImageSerializer(many=True)

    class Meta:
        model = User
        fields = ('phone_number', 'place_images')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'user', 'place', 'text', 'created_date')


class CreateFriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relation
        fields = ('id', 'follower', 'following')


class FollowersSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Relation
        fields = ('phone_number', 'first_name', 'last_name', 'profile_image')

    def get_phone_number(self, obj):
        return obj.follower.phone_number

    def get_first_name(self, obj):
        return obj.follower.first_name

    def get_last_name(self, obj):
        return obj.follower.last_name

    def get_profile_image(self, obj):
        return settings.MEDIA_URL + obj.follower.profile_image.name


class FollowingsSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Relation
        fields = ('phone_number', 'first_name', 'last_name', 'profile_image')

    def get_phone_number(self, obj):
        return obj.following.phone_number

    def get_first_name(self, obj):
        return obj.following.first_name

    def get_last_name(self, obj):
        return obj.following.last_name

    def get_profile_image(self, obj):
        return settings.MEDIA_URL + obj.following.profile_image.name


class RelationSerializer(serializers.ModelSerializer):
    followers = FollowersSerializer(many=True)
    followings = FollowingsSerializer(many=True)

    class Meta:
        model = User
        fields = ('followers', 'followings')


class UploadPlaceImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaceImage
        fields = ('id', 'user', 'place', 'image')


class FavoritePlaceSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    place_image = serializers.SerializerMethodField()
    overall_score = serializers.SerializerMethodField()
    place_types = serializers.SerializerMethodField()

    class Meta:
        model = FavoritePlace
        fields = ('id', 'name', 'place_image', 'overall_score', 'place_types')

    def get_id(self, obj):
        return obj.place.id

    def get_name(self, obj):
        return obj.place.name

    def get_place_image(self, obj):
        return settings.MEDIA_URL + obj.place.place_image.name

    def get_overall_score(self, obj):
        all_scores = obj.place.place_scores.all()
        average = 0
        for score in all_scores:
            average += score.total_score
        if len(all_scores) > 0:
            return round((average / len(all_scores)), 1)
        return 0

    def get_place_types(self, obj):
        all_types = obj.place.place_types.all()
        types_name = []
        for place_type in all_types:
            types_name.append(place_type.type)
        return types_name


class FavoritePlacesSerializer(serializers.ModelSerializer):
    favorite_places = FavoritePlaceSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'favorite_places')


class CreateFavoritePlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoritePlace
        fields = ('id', 'user', 'place')


class ReviewVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewVote
        fields = ('user', 'review', 'vote')


class PlaceImageVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaceImageVote
        fields = ('user', 'place_image', 'vote')


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ('place', 'review', 'name')
