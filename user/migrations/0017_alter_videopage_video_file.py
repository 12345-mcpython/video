# Generated by Django 4.1.4 on 2023-01-21 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_videopage_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videopage',
            name='video_file',
            field=models.FileField(upload_to='temp/wait'),
        ),
    ]