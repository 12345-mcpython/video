# Generated by Django 4.1.4 on 2022-12-30 19:56

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_user_comment_like_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='comment_like_list',
            field=models.JSONField(default=user.models.get_list),
        ),
        migrations.AlterField(
            model_name='user',
            name='video_like_list',
            field=models.JSONField(default=user.models.get_list),
        ),
    ]
