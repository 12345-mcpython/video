import os

import django
from celery import Celery
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video.settings')

django.setup()

app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379')


@app.task
def send_email(code, email):
    subject = '{}认证码'.format(settings.TITLE)

    text_content = '''感谢登录{}. \n登录认证码是{}. \n此链接有效期为{}天! \n 请不要回复本邮件!'''.format(
        settings.TITLE, code, 7)

    html_content = '''
                    <p>感谢登录{}.</p>
                    <p>登录认证码是{}.</p>
                    <p>此链接有效期为{}h!</p>
                    <p>请不要回复本邮件!</p>
                    '''.format(settings.TITLE, code, 2)

    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
