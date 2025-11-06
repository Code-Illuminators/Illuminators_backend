from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import BigfootPost, UfoPost, GhostPost, OtherPost

User = get_user_model()


class BasePostSerializer(serializers.ModelSerializer):
    """Abstract base serializer """
    image = serializers.CharField()
    owner = serializers.CharField()

    class Meta:
        """Class Meta for BasePostSerializer"""
        fields = '__all__'
        abstract = True

    def create(self, validated_data):
        image_path = validated_data.pop('image', None)
        owner_username = validated_data.pop('owner', None)

        if owner_username:
            try:
                validated_data['owner'] = User.objects.get(username=owner_username.split()[0])
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "owner": f"User with username '{owner_username}' does not exist."
                })

        instance = super().create(validated_data)
        if image_path:
            instance.image = image_path
        instance.save()
        return instance


class BigfootPostSerializer(BasePostSerializer):
    """Serializer for Bigfoot"""
    class Meta(BasePostSerializer.Meta):
        """Class Meta for BigfootPostSerializer"""
        model = BigfootPost


class UfoPostSerializer(BasePostSerializer):
    """Serializer for Ufo"""
    class Meta(BasePostSerializer.Meta):
        """Class Meta for UfoPostSerializer"""
        model = UfoPost


class GhostPostSerializer(BasePostSerializer):
    """Serializer for Ghost"""
    class Meta(BasePostSerializer.Meta):
        """Class Meta for GhostPostSerializer"""
        model = GhostPost


class OtherPostSerializer(BasePostSerializer):
    """Serializer for Other"""
    class Meta(BasePostSerializer.Meta):
        """Class Meta for OtherPostSerializer"""
        model = OtherPost
