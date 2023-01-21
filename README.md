# Video

一个类b站开放视频平台, 基于python3+django+redis+mysql.

## 功能

1. 登录(好像就写了登录接口)
2. 用户中心

## 运行

1. pip install -r requirements.txt
2. 配置config.json mysql redis
3. 运行celery celery -A video.tasks worker -l INFO -P eventlet
4. (可选) hub install porn_detection_lstm==1.1.0, hub serving start -m porn_detection_lstm 运行测黄工具