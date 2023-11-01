from rest_framework import viewsets

from apps.mxz_timeimprint.models import MxzDateEvent
from apps.mxz_timeimprint.serializer import MxzDateEventSerializer


# Create your views here.
class MxzDateEventViewSet(viewsets.ModelViewSet):
    queryset = MxzDateEvent.objects.all()
    serializer_class = MxzDateEventSerializer
