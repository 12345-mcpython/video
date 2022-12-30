import time

from django.test import TestCase
from django.core import mail


class LoginTest(TestCase):
    def test_login_by_email(self):
        captcha_key = self.client.post("/api/v1/email/user/send_code",
                                       data={"email": "a@b.com", "test_only": True}).json()['data'][
            'captcha_key']
        test_mail = mail.outbox[0].body
        for i in test_mail.split("\n"):
            if i.startswith("登录认证码是"):
                code = i.lstrip("登录认证码是")[:-2]
                break
        request = self.client.post("/api/v1/email/user",
                                   data={"email": "a@b.com", "captcha_key": captcha_key,
                                         "code": code}).json()

        self.assertEqual(request['code'], 0)
        self.assertEqual(request['msg'], "新用户登录成功!")
        # 重新登录老用户
        captcha_key = self.client.post("/api/v1/email/user/send_code",
                                       data={"email": "a@b.com", "test_only": True}).json()['data'][
            'captcha_key']
        test_mail = mail.outbox[1].body
        for i in test_mail.split("\n"):
            if i.startswith("登录认证码是"):
                code = i.lstrip("登录认证码是")[:-2]
                break
        request = self.client.post("/api/v1/email/user",
                                   data={"email": "a@b.com", "captcha_key": captcha_key,
                                         "code": code}).json()

        self.assertEqual(request['code'], 0)
        self.assertEqual(request['msg'], "老用户登录成功!")

    def test_incorrect_login(self):
        request = self.client.post("/api/v1/email/user",
                                   data={"email": "a@b.com", "captcha_key": "12354",
                                         "code": 123345}).json()
        self.assertEqual(request['code'], 10002)
        self.assertEqual(request['msg'], "用户未发送过邮箱验证码!")
        captcha_key = self.client.post("/api/v1/email/user/send_code",
                                       data={"email": "a@b.com", "test_only": True}).json()['data'][
            'captcha_key']
        test_mail = mail.outbox[0].body
        for i in test_mail.split("\n"):
            if i.startswith("登录认证码是"):
                code = i.lstrip("登录认证码是")[:-2]
                break
        request = self.client.post("/api/v1/email/user",
                                   data={"email": "a@b.com", "captcha_key": "123456",
                                         "code": code}).json()

        self.assertEqual(request['code'], 10003)
        self.assertEqual(request['msg'], "captcha_key认证失败!")
        request = self.client.post("/api/v1/email/user",
                                   data={"email": "a@b.com", "captcha_key": captcha_key,
                                         "code": "1"}).json()

        self.assertEqual(request['code'], 10004)
        self.assertEqual(request['msg'], "邮箱验证码错误!")
        request = self.client.post("/api/v1/email/user",
                                   data={"email": "a@b.com", "captcha_key": captcha_key,
                                         "code": code}).json()

        self.assertEqual(request['code'], 0)
        self.assertEqual(request['msg'], "新用户登录成功!")
        # 重复登录
        request = self.client.post("/api/v1/email/user",
                                   data={"email": "a@b.com", "captcha_key": captcha_key,
                                         "code": code}).json()

        self.assertEqual(request['code'], 10002)
        self.assertEqual(request['msg'], "用户未发送过邮箱验证码!")
