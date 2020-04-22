from rest_framework import serializers
from .models import TransWalk



class TranswalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransWalk
        fields = ('ASRid', 'Audio_File_Link', 'audio_duration') 