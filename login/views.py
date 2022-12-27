import base64
import random
import time
import uuid

from Crypto.Cipher import AES
from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from video import tasks

from .models import User

aes = AES.new(settings.SECRET_KEY.encode(), AES.MODE_ECB)


def index(request: HttpRequest):
    return JsonResponse({"code": 200, "msg": "API index", "data": {}})


@csrf_exempt
def login(request: HttpRequest):
    message = ""
    if request.POST:
        email = request.POST.get("email")
        user_email_code = request.POST.get("code")
        user_captcha_key = request.POST.get("captcha_key")
        if not cache.get(email + "_verify"):
            return JsonResponse({"code": 10002, "msg": "用户未发送过邮箱验证码!", "data": {}})
        captcha_key, email_code = cache.get(email + "_verify").split("|")
        if captcha_key != user_captcha_key:
            return JsonResponse({"code": 10003, "msg": "captcha_key认证失败!", "data": {}})
        if email_code != user_email_code:
            return JsonResponse({"code": 10004, "msg": "邮箱验证码错误!", "data": {}})
        try:
            user = User.objects.get(email=email)
            user_session_id = user.email + "|" + \
                str(int(time.time())) + "|"  + settings.SECRET_KEY
            user_session_id = aes.encrypt(user_session_id.encode())
            user_session_id = base64.b64encode(user_session_id)
            return JsonResponse({"code": 0, "msg": "老用户登录成功!", "data": {"session_id": user_session_id.decode()}})
        except User.DoesNotExist:
            new_user = User()
            new_user.name = "用户" + captcha_key
            new_user.email = email
            new_user.save()
            user_session_id = new_user.email + "|" + \
                str(int(time.time())) + "|"  + settings.SECRET_KEY
            user_session_id = aes.encrypt(user_session_id.encode())
            user_session_id = base64.b64encode(user_session_id)
            return JsonResponse({"code": 0, "msg": "新用户登录成功!", "data": {"session_id": user_session_id.decode()}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response


@csrf_exempt
def send_code(request: HttpRequest):
    if request.POST:
        email = request.POST.get("email")
        if cache.get(email) == "sent" and not is_test:
            return JsonResponse({"code": 10001, "msg": "发送太频繁! 等待100s后再试! ", "data": {}})
        code = random.randint(100000, 999999)
        captcha_key = uuid.uuid4().hex
        key = captcha_key + "|" + str(code)
        cache.set(email + "_verify", key, 60 * 60 * 2)
        cache.set(email, "sent", 100)
        tasks.send_email.delay(code, email)
        return JsonResponse({"code": 0, "msg": "发送成功: " + email, "data": {"captcha_key": captcha_key}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response
