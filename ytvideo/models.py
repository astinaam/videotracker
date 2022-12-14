from django.db import models
from ytvideo.managers import YTVideoStatManager, YTVideoTagManager

# Create your models here.

class YTVideoStat(models.Model):
    id = models.AutoField(primary_key=True)
    channelId = models.CharField(max_length=255)
    videoId = models.CharField(max_length=255)
    title = models.TextField(default="")
    viewCount = models.BigIntegerField(default=0)
    likeCount = models.BigIntegerField(default=0)
    favoriteCount = models.BigIntegerField(default=0)
    commentCount = models.BigIntegerField(default=0)
    videoPerformance = models.BigIntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    objects = YTVideoStatManager()
    
    def __str__(self) -> str:
        return f"Video: {self.videoId} Views: {self.viewCount} Performace: {self.videoPerformance}"
    
class YTVideoTag(models.Model):
    id = models.AutoField(primary_key=True)
    channelId = models.CharField(max_length=255)
    videoId = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    
    objects = YTVideoTagManager()
    
    def __str__(self) -> str:
        return f"Channel: {self.channelId} Video: {self.videoId} Tag: {self.tag}"
