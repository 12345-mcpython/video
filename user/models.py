from django.db import models
from taggit.managers import TaggableManager


def get_list():
    return []


class User(models.Model):
    name = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(unique=True)
    # 1 Lv1 2 Lv2 ... max Lv10
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    is_vip = models.BooleanField(default=False)
    description = models.TextField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatar', default="avatar/default.png")
    register_time = models.DateTimeField(auto_now_add=True)
    video_like_list = models.JSONField(default=get_list)
    comment_like_list = models.JSONField(default=get_list)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-register_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Follow(models.Model):
    follower = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="follower_user")
    followed = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name="followed_user")


class Video(models.Model):
    title = models.CharField(max_length=30)
    publish_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=300, default="", blank=True)
    cover = models.ImageField(upload_to='cover', default="cover/default.png")
    view = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    share = models.IntegerField(default=0)
    danmaku = models.IntegerField(default=0)
    author = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    examine = models.IntegerField(default=0)
    # 视频长度
    length = models.IntegerField(default=0)
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish_date"]
        verbose_name = "视频"
        verbose_name_plural = "视频"


class VideoPage(models.Model):
    page_title = models.CharField(max_length=15)
    video = models.ForeignKey(to=Video, on_delete=models.DO_NOTHING)
    video_file = models.FileField(upload_to="temp/wait")

    class Meta:
        ordering = ["-id"]
        verbose_name = "视频"
        verbose_name_plural = "视频"


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    like = models.IntegerField()
    is_topping = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    video = models.ForeignKey(to=Video, on_delete=models.DO_NOTHING)
    publish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-publish_date"]
        verbose_name = "评论"
        verbose_name_plural = "评论"


class CommentReply(models.Model):
    content = models.CharField(max_length=1000)
    like = models.IntegerField()
    is_topping = models.BooleanField(default=False)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(to=Comment, on_delete=models.DO_NOTHING)
    publish_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-publish_date"]
        verbose_name = "评论回复"
        verbose_name_plural = "评论回复"


class ExamineList(models.Model):
    video = models.ForeignKey(to=Video, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    status = models.IntegerField()