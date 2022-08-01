from django.conf import settings
import os
import environ
env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, '.env'))

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = env("YOUTUBE_API_KEY")
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def getAllVideosOfChannel(channelId):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, 
                    developerKey=DEVELOPER_KEY)

    videos = []
    nextPageToken = None
    while True:
        try:
            searchResponse = youtube.search().list(
                channelId=channelId,
                part='id,snippet',
                maxResults=50,
                pageToken=nextPageToken
            ).execute()
            nextPageToken = searchResponse.get('nextPageToken', None)
            for searchResult in searchResponse.get('items', []):
                if searchResult['id']['kind'] == 'youtube#video':
                    videos.append(searchResult['id']['videoId'])
            break
            if not nextPageToken:
                break
        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
            break
        except Exception as e:
            print(str(e))
            break
            
    return videos

