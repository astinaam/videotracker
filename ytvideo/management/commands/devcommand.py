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

    def fetchVideos(self, channelId):
        videoIds = []
        # Check if the videos for the channel is already fetched
        isChannelScanned = YTVideoStat.objects.isChannelScanned(channelId)
        if not isChannelScanned:
            print("Fetching video list from youtube api...")
            videoIds = yt.getAllVideosOfChannel(channelId)
        else:
            print("Fetching video list from database...")
            dbVids = YTVideoStat.objects.filter(channelId__exact=channelId).values_list('videoId')
            videoIds = [x[0] for x in dbVids]
        return videoIds
    
    def updateVideoStats(self, video):
        try:
            _stat = YTVideoStat.objects.update_or_create(
                videoId=video["videoId"],
                defaults={
                    'videoId':video["videoId"],
                    'channelId':video["channelId"],
                    'title': video["title"],
                    'viewCount': video["viewCount"],
                    'likeCount': video["likeCount"],
                    'favoriteCount': video["favoriteCount"],
                    'commentCount': video["commentCount"],
                }
            )
            print(_stat)
        except Exception as e:
            print("Exception occured when updating stats: %s" % str(e))
    
    def calculateMedianViews(self, channelId):
        channelStat = YTVideoStat.objects.filter(channelId__exact=channelId)
        videosCount = channelStat.count()
        values = channelStat.values_list("viewCount", flat=True).order_by("viewCount");
        medianViews = values[int(round(videosCount/2))]
        if videosCount % 2 == 0:
            medianViews = sum(values[videosCount/2-1:videosCount/2+1]) / 2.0
        return medianViews

    def updateVideoPerformance(self, channelId):
        # 10 minutes offset to ensure catching multiple the latest first hour stats fecthed
        firstHourVideoList = YTVideoStat.objects.filter(
            channelId=channelId, createdAt__gte=Now()-timedelta(hours=1, minutes=10)
        ).order_by('-createdAt').all()
        print("Found %d videos to update with first hour performance" % (len(firstHourVideoList)))
        if len(firstHourVideoList):
            medianViews = self.calculateMedianViews(channelId=channelId)
            # use the median value to update video performance value
            for videoStat in firstHourVideoList:
                performance = round(videoStat.viewCount / medianViews, 2)
                videoStat.videoPerformance = performance
                videoStat.save()
                print(videoStat, videoStat.viewCount, "Median views: ",medianViews)

    def handle(self, *args, **options):
        self.stdout.write("Running devcommand...")
        # self.stdout.write("Checking channels: %s" % (env("CHANNEL_LIST")))
        channelListCommaSep = env("CHANNEL_LIST")
        channelList = channelListCommaSep.split(",")
        # For each channel check the video stats
        for channelId in channelList:
            print("Handling for channelId:" + channelId)

            # Check if the tags for the channel is already fetched
            tagInsertedAlready = YTVideoTag.objects.isTagInsertedAlready(channelId)

            # Fetch video ids
            videoIds = self.fetchVideos(channelId=channelId)
            
            # Check and update video stats for each videos
            print("Updating video stats of %d videos..." % (len(videoIds)))
            VIDEOS_PER_REQUEST = 50
            for i in range(0, len(videoIds), VIDEOS_PER_REQUEST):
                currLen = min(i+VIDEOS_PER_REQUEST, len(videoIds))
                ids = ",".join(videoIds[i:currLen])
                videos = yt.getVideoList(ids)
                tagObjects = []
                for j in range(len(videos)):
                    self.updateVideoStats(video=videos[j])
                    # for each video update tags if not already updated
                    if not tagInsertedAlready:
                        for tag in videos[j]["tags"]:
                            tagObjects.append(
                                YTVideoTag(channelId=channelId, videoId=videos[j]["videoId"], tag=tag)
                            )
                if len(tagObjects):
                    print("Inserting %d tags" % (len(tagObjects)))
                    YTVideoTag.objects.bulk_create(tagObjects)

            # Update performace measure based on first hour views
            self.updateVideoPerformance(channelId=channelId)
