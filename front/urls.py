"""video URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('create/', views.create),
    path("create/upload/video/", views.upload_video),
    path("user_center/", views.user_center),
    path("user_center/edit_information/", views.edit_information),
    path("user_center/edit_avatar/", views.edit_avatar),
    path("use_agreement/", views.use_agreement),
    path("creative_convention/", views.creative_convention),
    path("create/upload_queue/", views.upload_queue),
    path("create/examine_queue/", views.examine_queue),
    path("create/moderate/examine/", views.examine)
]
