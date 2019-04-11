"""untitled URL Configuration

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
    path('user/', views.UserList.as_view()),
    path('user/<int:phone_number>/', views.UserDetail.as_view()),
    path('place/<int:pk>/', views.PlaceDetail.as_view()),
    path('place_menu/<int:pk>/', views.MenuDetail.as_view()),
    path('place_review/<int:pk>/', views.PlaceReview.as_view()),
    path('user_review/<int:phone_number>/', views.UserReview.as_view()),
    path('score/', views.Score.as_view()),
    path('review/', views.Review.as_view()),
    path('friend/', views.CreateFriend.as_view()),
    path('friend/<int:phone_number>/', views.Friend.as_view()),
] + static(settings.PHOTOS_URL, document_root=settings.PHOTOS_ROOT)
