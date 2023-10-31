from rest_framework import viewsets

from apps.timeimprint.models import DateEvent
from apps.timeimprint.serializer import DateEventSerializer


# Create your views here.
class DateEventViewSet(viewsets.ModelViewSet):
    queryset = DateEvent.objects.all()
    serializer_class = DateEventSerializer
