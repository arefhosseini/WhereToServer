from django.contrib import admin
from .models import User, Place, Review, PlaceScore, Hashtag, Menu, Relation, Token, FavoritePlaceType
from .models import FavoritePlace, Food, CoordinatePlace, PhonePlace, PlaceImage, PlaceType

admin.site.register(Token)
admin.site.register(User)
admin.site.register(Place)
admin.site.register(Review)
admin.site.register(PlaceScore)
admin.site.register(Hashtag)
admin.site.register(Relation)
admin.site.register(Menu)
admin.site.register(FavoritePlace)
admin.site.register(Food)
admin.site.register(CoordinatePlace)
admin.site.register(PhonePlace)
admin.site.register(PlaceImage)
admin.site.register(PlaceType)
admin.site.register(FavoritePlaceType)
