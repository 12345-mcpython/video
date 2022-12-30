import random
import re
import time
import uuid

import requests
from PIL import Image, UnidentifiedImageError
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from video import tasks

from .models import User


def verify_session_key(key: str):
    if not key:
        return False
    email, time_login, secret_key = key.split("|")
    if int(time_login) + settings.LOGIN_TIME <= time.time():
        return False
    elif secret_key != settings.SECRET_KEY:
        return False
    return email


def index(request: HttpRequest):
    return JsonResponse({"code": 200, "msg": "API index", "data": {}})


@csrf_exempt
def login(request: HttpRequest):
    if request.method == "POST":
        session: User = request.session.get('user')
        if session:
            return JsonResponse({"code": 10006, "msg": "账号已登录!", "data": {}})
        email = request.POST.get("email")
        user_email_code = request.POST.get("code")
        user_captcha_key = request.POST.get("captcha_key")

        pat = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
        if not email or (not re.match(pat, email)):
            return JsonResponse({"code": 10005, "msg": "邮箱格式错误!", "data": {}})
        if not cache.get(email + "_verify"):
            return JsonResponse({"code": 10002, "msg": "用户未发送过邮箱验证码!", "data": {}})
        captcha_key, email_code = cache.get(email + "_verify").split("|")
        if captcha_key != user_captcha_key:
            return JsonResponse({"code": 10003, "msg": "captcha_key认证失败!", "data": {}})
        if email_code != user_email_code:
            return JsonResponse({"code": 10004, "msg": "邮箱验证码错误!", "data": {}})
        add_new_user = False
        try:
            login_user = User.objects.get(email=email)
        except User.DoesNotExist:
            login_user = User()
            login_user.name = "用户" + captcha_key
            login_user.email = email
            login_user.save()
            add_new_user = True
        request.session["user"] = login_user
        cache.delete(email + "_verify")
        return JsonResponse({"code": 0, "msg": "新用户登录成功!" if add_new_user else "老用户登录成功!", "data": {}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response


@csrf_exempt
def send_code(request: HttpRequest):
    if request.method == "POST":
        session: User = request.session.get('user')
        if session:
            return JsonResponse({"code": 10006, "msg": "账号已登录!", "data": {}})
        email = request.POST.get("email")
        if not email:
            return JsonResponse({"code": 10005, "msg": "邮箱格式错误!", "data": {}})
        pat = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
        if not re.match(pat, email):
            return JsonResponse({"code": 10005, "msg": "邮箱格式错误!", "data": {}})
        is_test = request.POST.get("test_only")
        if cache.get(email) == "sent" and (not is_test and settings.DEBUG):
            return JsonResponse({"code": 10001, "msg": "发送太频繁! 等待100s后再试! ", "data": {}})
        if is_test and settings.DEBUG:
            code = 0
        else:
            code = random.randint(100000, 999999)
        captcha_key = uuid.uuid4().hex
        key = captcha_key + "|" + str(code)
        cache.set(email + "_verify", key, 60 * 60 * 2)
        cache.set(email, "sent", 100)
        if is_test and settings.DEBUG:
            tasks.send_email(code, email)
        else:
            tasks.send_email.delay(code, email)
        return JsonResponse({"code": 0, "msg": "发送成功: " + email, "data": {"captcha_key": captcha_key}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response


def account(request: HttpRequest):
    session: User = request.session.get('user')
    if not session:
        return JsonResponse({"code": 10006, "msg": "账号未登录!", "data": {}})
    return JsonResponse(
        {"code": 0, "msg": "", "data": {"mid": session.pk, "uname": session.name}})


@csrf_exempt
def logout(request: HttpRequest):
    if request.method == "POST":
        session: User = request.session.get('user')
        if not session:
            return JsonResponse({"code": 10006, "msg": "账号未登录!", "data": {}})
        else:
            del request.session["user"]
            return JsonResponse({"code": 0, "msg": "退出登录成功!", "data": {}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response


@csrf_exempt
def edit_information(request):
    if request.method == "POST":
        session: User = request.session.get('user')
        if not session:
            return JsonResponse({"code": 10006, "msg": "账号未登录!", "data": {}})
        username = request.POST.get("username")
        description = request.POST.get("description")
        session: User = request.session.get('user')
        if username:
            verify_username = tasks.verify_text.delay(username)
            is_yellow = verify_username.get()
            print(is_yellow)
            if is_yellow:
                return JsonResponse({"code": 10010, "msg": "用户名含有黄色内容!", "data": {}})
            if len(username) >= 16:
                return JsonResponse({"code": 10007, "msg": "用户名长度不得超过16字符!", "data": {}})
            session.name = username
        if description:
            verify_description = tasks.verify_text.delay(description)
            is_yellow = verify_description.get()
            print(is_yellow)
            if is_yellow:
                return JsonResponse({"code": 10010, "msg": "个性签名含有黄色内容!", "data": {}})
            if len(description) >= 500:
                return JsonResponse({"code": 10007, "msg": "个人签名长度不得超过500字符!", "data": {}})
            session.description = description
        session.save()
        request.session['user'] = session
        return JsonResponse({"code": 0, "msg": "修改信息成功!", "data": {}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response


@csrf_exempt
def edit_avatar(request):
    if request.method == "POST":
        session: User = request.session.get('user')
        if not session:
            return JsonResponse({"code": 10006, "msg": "账号未登录!", "data": {}})
        icon: InMemoryUploadedFile = request.FILES.get("avatar")
        if not icon:
            return JsonResponse({"code": 10009, "msg": "图片格式错误!", "data": {}})
        try:
            image = Image.open(icon)
        except UnidentifiedImageError:
            return JsonResponse({"code": 10009, "msg": "图片格式错误!", "data": {}})
        icon.seek(0)
        icon.name += ("." + image.format.lower())
        # icon = BytesIO(image.tobytes())
        if image.format.lower() not in ["png", "jpeg"]:
            return JsonResponse({"code": 10009, "msg": "图片格式错误!", "data": {}})
        width, height = image.size
        if width > 512 or height > 512:
            return JsonResponse({"code": 10008, "msg": "图片尺寸大于512x512!", "data": {}})
        session: User = request.session.get('user')
        session.avatar = icon
        session.save()
        request.session['user'] = session
        return JsonResponse({"code": 0, "msg": "修改头像成功!", "data": {}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response
