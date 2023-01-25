import json
import os

import django
import requests
from celery import Celery
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from obs import ObsClient
from user.models import Video

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video.settings')

django.setup()

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

client = ObsClient(
    access_key_id=settings.OSS_ACCESS_KEY,
    secret_access_key=settings.OSS_SECRET_KEY,
    server=settings.OSS_ENDPOINT)


@app.task
def send_email(code, email):
    subject = '{}认证码'.format(settings.TITLE)

    text_content = '''感谢登录{}. \n登录认证码是{}. \n此认证码有效期为{}小时! \n 请不要回复本邮件!'''.format(
        settings.TITLE, code, 2)

    html_content = '''
                    <p>感谢登录{}.</p>
                    <p>登录认证码是{}.</p>
                    <p>此认证码有效期为{}小时!</p>
                    <p>请不要回复本邮件!</p>
                    '''.format(settings.TITLE, code, 2)

    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@app.task
def verify_text(text):
    if not settings.PORN_VERIFY:
        return False
    data = {"texts": [text], "batch_size": 1, "use_gpu": False}
    headers = {"Content-Type": "application/json"}
    url = settings.PORN_VERIFY + "/predict/porn_detection_lstm"
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    if r.json()['results'][0]['porn_probs'] > 0.04:
        return True
    else:
        return False


@app.task()
def upload_video(video, name, video_id):
    sum_bytes_out = 0
    times_out = 0
    video_object = Video.objects.filter(id=video_id).first()

    def upload_state(update_bytes, sum_bytes, times):
        nonlocal sum_bytes_out
        nonlocal times_out
        sum_bytes_out = sum_bytes
        times_out = times
        upload_video.update_state(state='PROGRESS', meta={'progress': round(update_bytes / sum_bytes * 100, 2),
                                                          "update_bytes": update_bytes, "sum_bytes": sum_bytes,
                                                          "times": times, "video": video_object})

    resp = client.putContent(settings.OSS_BUCKET, name, content=video.read(), progressCallback=upload_state)
    if resp.status > 300:
        upload_video.update_state(state='ERROR',
                                  meta={"error_code": resp.errorCode, "error_message": resp.errorMessage,
                                        "video": video_object})
    upload_video.update_state(state='SUCCESSFUL',
                              meta={"sum_bytes": sum_bytes_out, "time": times_out, "video": video_object})
