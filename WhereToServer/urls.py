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
    path('verify/', views.Verify.as_view()),
    path('user/', views.UserList.as_view()),
    path('user/upload/', views.UploadUserProfile.as_view()),
    path('user/<str:your_phone_number>/<str:user_phone_number>/', views.UserDetail.as_view()),
    path('places/<str:phone_number>/', views.PlaceList.as_view()),
    path('place/<str:phone_number>/<int:pk>/', views.PlaceDetail.as_view()),
    path('place/upload/', views.UploadPlaceImage.as_view()),
    path('place_menu/<int:pk>/', views.MenuDetail.as_view()),
    path('place_review/<int:pk>/', views.PlaceReviewDetail.as_view()),
    path('user_review/<str:phone_number>/', views.UserReviewDetail.as_view()),
    path('score/', views.ScoreDetail.as_view()),
    path('review/', views.ReviewDetail.as_view()),
    path('friend/', views.EditFriend.as_view()),
    path('friend/<str:your_phone_number>/<str:user_phone_number>/', views.GetFriend.as_view()),
    path('favorite_place/<str:phone_number>/', views.GetFavoritePlace.as_view()),
    path('favorite_place/', views.EditFavoritePlace.as_view()),
] + static(settings.PHOTOS_URL, document_root=settings.PHOTOS_ROOT)
