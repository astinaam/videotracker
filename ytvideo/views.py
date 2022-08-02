from django.shortcuts import render
from urllib import request
from django.http import HttpResponse
from rest_framework import viewsets

from .serializers import YTVideoSerializer
from .models import YTVideoStat

def HomeView(request, *args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")

class YTVideoStatViewSet(viewsets.ModelViewSet):
    queryset = YTVideoStat.objects.all()
    serializer_class = YTVideoSerializer

