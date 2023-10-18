from rest_framework import serializers
from timeimprint.models import DateEvent


class DateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateEvent
        fields = '__all__'
