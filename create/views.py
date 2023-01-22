from django.http import HttpRequest, JsonResponse
import cv2
from django.views.decorators.csrf import csrf_exempt

from user.models import User, Video, VideoPage


@csrf_exempt
def upload_video(request: HttpRequest):
    if request.method == "POST":
        session: User = request.session.get('user')
        if not session:
            return JsonResponse({"code": 10006, "msg": "账号未登录!", "data": {}})
        video = Video()
        video.title = request.POST.get("title")
        video.description = request.POST.get("description")
        video.cover = request.FILES.get("avatar")
        video_page = VideoPage()
        cv2.Video

        video_page.page_title = request.POST.get("title")
        video_page.video_file = request.FILES.get("files")
        video_page.video = video
        return JsonResponse({"code": 0, "msg": "上传成功, 等待审核", "data": {}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response
