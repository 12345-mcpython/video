# Generated by Django 4.1.4 on 2022-12-30 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
