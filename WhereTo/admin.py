from django.contrib import admin
from .models import User, Place, Review, PlaceScore, Hashtag, Menu, Friend
from .models import FavoritePlace, Food, CoordinatePlace, PhonePlace, PlaceImage, PlaceType

admin.site.register(User)
admin.site.register(Place)
admin.site.register(Review)
admin.site.register(PlaceScore)
admin.site.register(Hashtag)
admin.site.register(Friend)
admin.site.register(Menu)
admin.site.register(FavoritePlace)
admin.site.register(Food)
admin.site.register(CoordinatePlace)
admin.site.register(PhonePlace)
admin.site.register(PlaceImage)
admin.site.register(PlaceType)
