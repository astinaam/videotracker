from django.db import models

class YTVideoStatManager(models.Manager):
    def isChannelScanned(self, channelId):
        try:
            channelStats = self.filter(channelId__exact=channelId)[:1]
            # print(channelStats)
            return len(channelStats) > 0
        except Exception as e:
            print(str(e))
            return False

class YTVideoTagManager(models.Manager):
    def isTagInsertedAlready(self, channelId):
        try:
            tags = self.filter(channelId__exact=channelId)[:1]
            # print(tags)
            return len(tags) > 0
        except Exception as e:
            print(str(e))
            return False
