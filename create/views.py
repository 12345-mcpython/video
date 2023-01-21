from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

from user.models import User, Video


@csrf_exempt
def upload_video(request: HttpRequest):
    if request.method == "POST":
        session: User = request.session.get('user')
        if not session:
            return JsonResponse({"code": 10006, "msg": "账号未登录!", "data": {}})
        video = Video()
        return JsonResponse({"code": 0, "msg": "上传成功, 等待审核", "data": {}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response
