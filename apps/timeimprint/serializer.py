from rest_framework import serializers
from apps.timeimprint.models import DateEvent


class DateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateEvent
        fields = '__all__'
