from rest_framework import serializers
from .models import BigfootPost, UfoPost, GhostPost, OtherPost

class BasePostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField()

    class Meta:
        fields = ['id', 'owner', 'location', 'image', 'created_at']

class BigfootPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        model = BigfootPost

class UfoPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        model = UfoPost

class GhostPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        model = GhostPost

class OtherPostSerializer(BasePostSerializer):
    class Meta(BasePostSerializer.Meta):
        model = OtherPost
