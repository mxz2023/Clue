from rest_framework import serializers
from apps.mxz_timeimprint.models import MxzDateEvent


class MxzDateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MxzDateEvent
        fields = '__all__'
