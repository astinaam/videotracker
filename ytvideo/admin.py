from django.contrib import admin

from .models import YTVideoStat, YTVideoTag

@admin.register(YTVideoStat)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", "channelId", "videoId", "viewCount", 
        "likeCount", "dislikeCount", "commentCount",
        "videoPerformance", "updatedAt"
    )


@admin.register(YTVideoTag)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id", "channelId", "videoId"
    )
