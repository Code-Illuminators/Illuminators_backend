from rest_framework import serializers
from .models import BigfootPost, UfoPost, GhostPost, OtherPost

class BasePostSerializer(serializers.ModelSerializer):
    """Base serializer for all post types."""
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField()

    class Meta:
        """Metadata for BasePostSerializer."""
        fields = ['id', 'owner', 'location', 'image', 'created_at']

class BigfootPostSerializer(BasePostSerializer):
    """Serializer for Bigfoot posts."""
    class Meta(BasePostSerializer.Meta):
        """Metadata for BigfootPostSerializer."""
        model = BigfootPost

class UfoPostSerializer(BasePostSerializer):
    """Serializer for Ufo posts."""
    class Meta(BasePostSerializer.Meta):
        """Metadata for UfoPostSerializer."""
        model = UfoPost

class GhostPostSerializer(BasePostSerializer):
    """Serializer for Ghost posts."""
    class Meta(BasePostSerializer.Meta):
        """Metadata for GhostPostSerializer."""
        model = GhostPost

class OtherPostSerializer(BasePostSerializer):
    """Serializer for other types of posts."""
    class Meta(BasePostSerializer.Meta):
        """Metadata for OtherPostSerializer."""
        model = OtherPost
