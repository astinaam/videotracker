from django.db import models

class YTVideoStatManager(models.Manager):
    def isChannelScanned(self, channelId):
        try:
            _channelStat = self.filter(channelId__exact=channelId)[:1]
            # print(_channelStat)
            return True
        except Exception as e:
            print(str(e))
            return False

class YTVideoTagManager(models.Manager):
    def isTagInsertedAlready(self, channelId):
        try:
            _tags = self.filter(channelId__exact=channelId)[:1]
            # print(_tags)
            return True
        except Exception as e:
            print(str(e))
            return False
