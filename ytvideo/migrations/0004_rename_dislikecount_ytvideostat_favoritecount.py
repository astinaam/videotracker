# Generated by Django 4.0.6 on 2022-08-01 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ytvideo', '0003_ytvideostat_createdat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ytvideostat',
            old_name='dislikeCount',
            new_name='favoriteCount',
        ),
    ]