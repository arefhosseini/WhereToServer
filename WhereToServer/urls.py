"""WhereToServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from WhereTo import views
urlpatterns = [
    path('admin/', admin.site.urls),

    path('user/', views.UserControl.as_view()),
    path('user/verify/', views.VerifyUser.as_view()),
    path('user/profile_image/', views.UploadUserProfile.as_view()),
    path('user/relation/', views.RelationControl.as_view()),
    path('user/favorite_place/', views.FavoritePlaceControl.as_view()),
    path('user/favorite_place_type/', views.FavoritePlaceTypeControl.as_view()),
    path('user/<str:your_phone_number>/<str:user_phone_number>/', views.UserDetail.as_view()),
    path('user/<str:your_phone_number>/<str:user_phone_number>/review/', views.UserReviewList.as_view()),
    path('user/<str:your_phone_number>/<str:user_phone_number>/place_score/', views.UserPlaceScoreList.as_view()),
    path('user/<str:your_phone_number>/<str:user_phone_number>/relation/', views.RelationList.as_view()),
    path('user/<str:your_phone_number>/<str:user_phone_number>/image/', views.UserImageList.as_view()),
    path('user/<str:your_phone_number>/<str:user_phone_number>/favorite_place/', views.FavoritePlaceList.as_view()),

    path('place/image/', views.UploadPlaceImage.as_view()),
    path('place/review/', views.ReviewControl.as_view()),
    path('place/score/', views.ScoreControl.as_view()),
    path('place/image/vote/', views.PlaceImageVoteControl.as_view()),
    path('place/review/vote/', views.ReviewVoteControl.as_view()),
    path('place/<str:phone_number>/', views.PlaceList.as_view()),
    path('place/<str:phone_number>/<int:pk>/', views.PlaceDetail.as_view()),
    path('place/<str:phone_number>/<int:pk>/review/', views.PlaceReviewList.as_view()),
    path('place/<str:phone_number>/<int:pk>/menu/', views.MenuList.as_view()),

    path('search/user/<str:text>/', views.SearchUser.as_view()),
    path('search/place/<str:text>/', views.SearchPlace.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
