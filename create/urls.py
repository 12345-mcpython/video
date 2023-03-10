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
from django.urls import path

from . import views

urlpatterns = [
    path('publish_video', views.publish_video),
    path('get_examine_speed', views.get_examine_speed),
    path("get_tasks", views.get_tasks),
    path("get_video", views.get_video),
    path("get_examine_list", views.get_examine_list),
    path("delete_error_tasks", views.delete_error_tasks),
    path('delete_all_tasks', views.delete_all_tasks)
]
