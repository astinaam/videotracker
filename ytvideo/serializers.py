from rest_framework import serializers
from .models import YTVideoStat

class YTVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YTVideoStat
        fields = (
            'channelId', 'videoId', 'title', 'viewCount', 'likeCount',
            'favoriteCount', 'commentCount', 'videoPerformance'
        )

