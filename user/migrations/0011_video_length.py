# Generated by Django 4.1.4 on 2022-12-30 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_user_comment_like_list_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='length',
            field=models.IntegerField(default=0),
        ),
    ]
