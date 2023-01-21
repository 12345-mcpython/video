from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.conf import settings


# Create your views here.
def index(request: HttpRequest):
    title = settings.TITLE
    user = request.session.get("user")
    return render(request, "index.html", locals())


def user_center(request: HttpRequest):
    title = settings.TITLE
    user = request.session.get("user")
    if not user:
        return redirect("/login/")
    return render(request, "user/user_center.html", locals())


def edit_information(request):
    title = settings.TITLE
    user = request.session.get("user")
    if not user:
        return redirect("/login/")
    return render(request, "user/edit_information.html", locals())


def edit_avatar(request):
    title = settings.TITLE
    user = request.session.get("user")
    if not user:
        return redirect("/login/")
    return render(request, "user/edit_avatar.html", locals())


def login(request):
    title = settings.TITLE
    user = request.session.get("user")
    if user:
        return redirect("/")
    return render(request, "login.html", locals())


def create(request):
    title = settings.TITLE
    user = request.session.get("user")
    if not user:
        return redirect("/login/")
    return render(request, "create/create.html", locals())


def upload_video(request):
    title = settings.TITLE
    user = request.session.get("user")
    if not user:
        return redirect("/login/")
    return render(request, "create/upload_video.html", locals())