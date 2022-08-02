from posixpath import basename
from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'videos', YTVideoStatList, basename="YTVideoStat")


urlpatterns = [
	path('', include(router.urls)),
]
