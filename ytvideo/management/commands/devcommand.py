from django.core.management.base import BaseCommand
from django.conf import settings
import os

import environ
env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))

import ytvideo.ytapi as yt
from ytvideo.models import YTVideoStat, YTVideoTag

from datetime import timedelta
from django.db.models.functions import Now

class Command(BaseCommand):
    help = "Dev command for development"

    def handle(self, *args, **options):
        self.stdout.write("Running dev command...")
        self.stdout.write("Channels: %s" % (env("CHANNEL_LIST")))
        # yt.getAllVideosOfChannel("UCHnyfMqiRRG1u-2MsSQLbXA")
        channelListCommaSep = env("CHANNEL_LIST")
        channelList = channelListCommaSep.split(",")
        # For each channel check the video stats
        for channelId in channelList:
            print("Handling for channelDd:" + channelId)
            # Check if the videos for the channel is already fetched
            channelFetched = False
            try:
                channelStat = YTVideoStat.objects.get(channelId__exact=channelId)
                channelFetched = True
                print(channelStat)
            except Exception as e:
                channelFetched = False

            tagInsertedAlready = False
            try:
                _tags = YTVideoTag.objects.get(channelId__exact=channelId)
                tagInsertedAlready = True
            except Exception as e:
                tagInsertedAlready = False

            videoIds = []
            if not channelFetched:
                print("fetching from youtube api...")
                videoIds = yt.getAllVideosOfChannel(channelId)
            else:
                print("fetching from database")
                dbVids = YTVideoStat.objects.filter(channelId__exact=channelId).values_list('videoId')
                videoIds = [x[0] for x in dbVids]
            # check and update video stats for each videos
            for i in range(0, len(videoIds), 10):
                remLen = len(videoIds) - i
                maxLen = min(i+10, i+remLen)
                # for each video update stats
                ids = ",".join(videoIds[i:maxLen])
                # print(ids)
                videos = yt.getVideoList(ids)
                # print(videos)
                tagObjects = []
                for j in range(len(videos)):
                    stat = YTVideoStat.objects.update_or_create(
                        videoId=videos[j]["videoId"],
                        defaults={
                            'videoId':videos[j]["videoId"],
                            'channelId':videos[j]["channelId"],
                            'title': videos[j]["title"],
                            'viewCount': videos[j]["viewCount"],
                            'likeCount': videos[j]["likeCount"],
                            'favoriteCount': videos[j]["favoriteCount"],
                            'commentCount': videos[j]["commentCount"],
                        }
                    )
                    # print(stat)
                    # for each video update tags if not already updated
                    if not tagInsertedAlready:
                        for tag in videos[j]["tags"]:
                            tagObjects.append(YTVideoTag(channelId=channelId, videoId=videos[j]["videoId"], tag=tag))
                if len(tagObjects):
                    YTVideoTag.objects.bulk_create(tagObjects)

            # Update performace measure based on first hour views
            videoStatsToUpdate = YTVideoStat.objects.filter(
                channelId=channelId, createdAt__gte=Now()-timedelta(hours=1)
            ).order_by('-createdAt').all()
            if len(videoStatsToUpdate):
                # find median views
                channelStat = YTVideoStat.objects.filter(channelId__exact=channelId)
                videosCount = channelStat.count()
                values = channelStat.values_list("viewCount", flat=True).order_by("viewCount");
                medianViews = values[int(round(videosCount/2))]
                if videosCount % 2 == 0:
                    medianViews = sum(values[videosCount/2-1:videosCount/2+1])/2.0
                # use the median value to update video performance value
                for videoStat in videoStatsToUpdate:
                    performance = round(videoStat.viewCount / medianViews, 2)
                    videoStat.videoPerformance = performance
                    videoStat.save()
                    print(videoStat, videoStat.viewCount, "Median views: ",medianViews)
