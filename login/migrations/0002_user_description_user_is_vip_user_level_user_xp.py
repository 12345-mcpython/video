# Generated by Django 4.1.4 on 2022-12-26 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_vip',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='xp',
            field=models.IntegerField(default=0),
        ),
    ]
