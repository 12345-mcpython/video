# Generated by Django 4.1.4 on 2022-12-31 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_video_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='user.user'),
        ),
    ]
