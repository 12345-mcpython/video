from django.db import models
from taggit.managers import TaggableManager


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    default = models.BooleanField(default=False, db_index=True)
    permissions = models.IntegerField()
    users = models.ForeignKey(to="User", on_delete=models.CASCADE)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.objects.filter(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            role.save()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


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
    roles = models.ForeignKey('Role', to_field="id", on_delete=models.CASCADE)

    def can(self, perm):
        return self.roles is not None and self.roles.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

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
    cover = models.ImageField(upload_to='cover/', default="cover/default.png")
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
    page_title = models.CharField(max_length=30)
    video = models.ForeignKey(to=Video, on_delete=models.DO_NOTHING)
    video_file = models.FileField(upload_to="temp/wait/")

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
