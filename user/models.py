from django.db import models


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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-register_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
