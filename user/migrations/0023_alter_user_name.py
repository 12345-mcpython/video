# Generated by Django 4.1.4 on 2023-01-25 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_alter_videopage_video_file_tasklist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]