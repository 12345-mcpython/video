from django.db import models


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256, null=True)
    email = models.EmailField(unique=True)
    # 1 Lv1 2 Lv2 ... max Lv10
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    is_vip = models.BooleanField(default=False)
    description = models.TextField(max_length=500, null=True)
    register_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-register_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"