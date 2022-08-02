from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'videos', YTVideoStatViewSet)


urlpatterns = [
	path('', include(router.urls)),
]
