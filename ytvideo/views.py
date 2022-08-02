from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets

from .serializers import YTVideoSerializer
from .models import YTVideoStat, YTVideoTag

def HomeView(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))

class YTVideoStatList(viewsets.ModelViewSet):
    serializer_class = YTVideoSerializer
    
    def get_queryset(self):
        queryset = YTVideoStat.objects.all()
        tag = self.request.query_params.get('tag')
        if tag is not None:
            matchedTags = YTVideoTag.objects.filter(tag__icontains=tag).values_list('videoId', flat=True)
            queryset = queryset.filter(videoId__in=list(matchedTags))

        sortByPerformance = self.request.query_params.get('sortByPerformance')
        if sortByPerformance is not None:
            order = "-videoPerformance"
            if sortByPerformance == "asc":
                order = "videoPerformance"
            queryset = queryset.order_by(order)
        return queryset
