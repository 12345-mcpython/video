from django.urls import path

from . import views

urlpatterns = [
    path("login/email/send_code", views.send_code),
    path("login/email", views.login),
    path("logout", views.logout),
    path("account", views.account),
    path("account/edit_information", views.edit_information),
    path("account/edit_avatar", views.edit_avatar),
]
