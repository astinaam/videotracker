# Generated by Django 4.0.6 on 2022-08-01 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YTVideoStat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('channelId', models.CharField(max_length=255)),
                ('videoId', models.CharField(max_length=255)),
                ('viewCount', models.BigIntegerField(default=0)),
                ('likeCount', models.BigIntegerField(default=0)),
                ('dislikeCount', models.BigIntegerField(default=0)),
                ('commentCount', models.BigIntegerField(default=0)),
                ('videoPerformance', models.BigIntegerField(default=0)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='YTVideoTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('channelId', models.CharField(max_length=255)),
                ('videoId', models.CharField(max_length=255)),
                ('tag', models.CharField(max_length=255)),
            ],
        ),
    ]
