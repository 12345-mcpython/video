import datetime

from django.http import HttpRequest
from django.shortcuts import render, redirect
from user.models import Permission, User
from django.conf import settings


# Create your views here.
def index(request: HttpRequest):
    title = settings.TITLE
    user = request.session.get("user")
    return render(request, "index.html", locals())


def use_agreement(request: HttpRequest):
    title = settings.TITLE
    user = request.session.get("user")
    date = datetime.datetime(year=2023, month=1, day=23)
    return render(request, "agreement/use_agreement.html", locals())


def dark_room(request: HttpRequest):
    title = settings.TITLE
    user = request.session.get("user")
    date = datetime.datetime(year=2023, month=1, day=23)
    return render(request, "agreement/dark_room.html", locals())


def creative_convention(request: HttpRequest):
    title = settings.TITLE
    user = request.session.get("user")
    date = datetime.datetime(year=2023, month=1, day=23)
    return render(request, "agreement/creative_convention.html", locals())


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
    moderate = False
    if user.can(Permission.MODERATE):
        moderate = True
    return render(request, "create/create.html", locals())


def upload_video(request):
    title = settings.TITLE
    user = request.session.get("user")
    if not user:
        return redirect("/login/")
    moderate = False
    if user.can(Permission.MODERATE):
        moderate = True
    return render(request, "create/upload_video.html", locals())


def upload_queue(request):
    title = settings.TITLE
    user = request.session.get("user")
    if not user:
        return redirect("/login/")
    moderate = False
    if user.can(Permission.MODERATE):
        moderate = True
    return render(request, "create/upload_queue.html", locals())


def examine_queue(request):
    title = settings.TITLE
    user = request.session.get("user")
    if not user:
        return redirect("/login/")
    moderate = False
    if user.can(Permission.MODERATE):
        moderate = True
    return render(request, "create/examine_queue.html", locals())

def examine(request):
    title = settings.TITLE
    user = request.session.get("user")
    if not user:
        return redirect("/login/")
    moderate = False
    if user.can(Permission.MODERATE):
        moderate = True
    return render(request, "create/examine.html", locals())
