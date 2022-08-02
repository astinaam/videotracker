from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets

from .serializers import YTVideoSerializer
from .models import YTVideoStat

def HomeView(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

class YTVideoStatViewSet(viewsets.ModelViewSet):
    queryset = YTVideoStat.objects.all()
    serializer_class = YTVideoSerializer

