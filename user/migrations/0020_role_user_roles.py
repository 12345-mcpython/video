# Generated by Django 4.1.4 on 2023-01-24 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_alter_video_cover_alter_videopage_video_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('default', models.BooleanField(db_index=True, default=False)),
                ('permissions', models.IntegerField()),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.role'),
        ),
    ]
