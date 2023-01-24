# Video

一个仿b站视频平台, 基于python3+django+redis+mysql.

## 功能

1. 使用邮箱登录
2. 用户中心 (3/4成品)
3. 投稿中心 (半成品)

## 将要实现的功能

1. 审核
2. 弹幕
3. 播放

## 运行

1. 确保你的python版本是3.8以上
2. 安装依赖 `pip install -r requirements.txt`
3. 按照config.example.json配置OSS, MySQL和Redis, 保存为config.json
4. 开启另一个命令行窗口运行celery `celery -A video.tasks worker -l INFO -P eventlet`
5. (可选,
   用于用户名和个性签名的鉴黄) <br> `hub install porn_detection_lstm==1.1.0` <br> `hub serving start -m porn_detection_lstm`
6. python manage.py runserver

## 备注

界面设计极其 ~~高端~~ 垃圾, 如果有好心人帮我修改可以发一下PR.

如果有安全漏洞请发email: m15043340061@163.com
