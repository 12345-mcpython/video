# Generated by Django 4.1.4 on 2022-12-26 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_user_description_user_is_vip_user_level_user_xp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
