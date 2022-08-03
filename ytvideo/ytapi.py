from time import sleep
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
            if not nextPageToken:
                break
            # Delay between requests
            sleep(.150)
        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
            break
        except Exception as e:
            print("Exception occured when searching videos: %s" % str(e))
            break
            
    return videos

def _getVideoAttribute(obj, key, defaultValue):
    if key in obj:
        return obj[key]
    return defaultValue

def getVideoList(ids):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, 
                    developerKey=DEVELOPER_KEY)
    videos = []
    nextPageToken = None
    while True:
        try:
            searchResponse = youtube.videos().list(
                part='id,snippet,statistics',
                id=ids,
                maxResults=50,
                pageToken=nextPageToken
            ).execute()
            nextPageToken = searchResponse.get('nextPageToken', None)
            videoItems = searchResponse.get('items', [])
            for searchResult in videoItems:
                # print(searchResult)
                video = {
                    "channelId": searchResult['snippet']['channelId'],
                    "videoId": searchResult['id'],
                    "title": _getVideoAttribute(searchResult['snippet'], 'title', 'Untitled'),
                    "tags": _getVideoAttribute(searchResult['snippet'], 'tags', []),
                    "viewCount": _getVideoAttribute(searchResult['statistics'], 'viewCount', 0),
                    "likeCount": _getVideoAttribute(searchResult['statistics'], 'likeCount', 0),
                    "favoriteCount": _getVideoAttribute(searchResult['statistics'], 'favoriteCount', 0),
                    "commentCount": _getVideoAttribute(searchResult['statistics'], 'commentCount', 0),
                }
                videos.append(video)
            if not nextPageToken:
                break
            # Delay between requests
            sleep(.150)
        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
            break
        except Exception as e:
            print("Exception occured when fetcing video list: %s" % str(e))
            break
            
    return videos