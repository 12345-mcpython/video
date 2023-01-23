from PIL import Image, UnidentifiedImageError
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.models import User, Video, VideoPage, ExamineList


@csrf_exempt
def publish_video(request: HttpRequest):
    if request.method == "POST":
        session: User = request.session.get('user')
        if not session:
            return JsonResponse({"code": 10006, "msg": "账号未登录!", "data": {}})

        file = request.FILES.get("files")
        cover = request.FILES.get("cover")
        title = request.POST.get("title")
        description = request.POST.get("description")
        tags = request.POST.get("tags")
        if not all([file, cover, title, description, tags]):
            return JsonResponse({"code": 10009, "msg": "信息不完整!", "data": {}})
        video = Video()
        video.title = title
        video.description = description

        try:
            image = Image.open(cover)
        except UnidentifiedImageError:
            return JsonResponse({"code": 10009, "msg": "图片格式错误!", "data": {}})

        cover.seek(0)
        cover.name += ("." + image.format.lower())

        if image.format.lower() not in ["png", "jpeg"]:
            return JsonResponse({"code": 10009, "msg": "图片格式错误!", "data": {}})

        width, height = image.size
        print(width, height)
        if width / height != 16 / 9:
            return JsonResponse({"code": 10008, "msg": "图片比例非16 : 9!", "data": {}})

        video.cover = cover
        video.author = request.session.get("user")
        video.save()
        video.tags.add(*tags.split(","))
        video.save()

        video_page = VideoPage()
        video_page.page_title = title
        video_page.video_file = file
        video_page.video = video
        video_page.save()
        examine = ExamineList()
        examine.video = video
        examine.user = request.session.get("user")
        examine.status = 0
        examine.save()
        return JsonResponse({"code": 0, "msg": "上传成功, 等待审核", "data": {}})
    else:
        response = JsonResponse(
            {"code": 405, "msg": "Method not allowed", "data": {}})
        response.status_code = 405
        return response


@csrf_exempt
def get_examine_speed(request):
    request.get_host()
    examine_total = ExamineList.objects.count()
    if examine_total < 100:
        return JsonResponse({"code": 0, "msg": "快速", "data": {'total': examine_total}})
    elif 100 < examine_total < 500:
        return JsonResponse({"code": 0, "msg": "中速", "data": {'total': examine_total}})
    elif 500 < examine_total < 1000:
        return JsonResponse({"code": 0, "msg": "缓慢", "data": {'total': examine_total}})
    elif examine_total > 1000:
        return JsonResponse({"code": 0, "msg": "极为缓慢", "data": {'total': examine_total}})
