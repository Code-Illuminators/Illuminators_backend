from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import BigfootPost, UfoPost, GhostPost, OtherPost

User = get_user_model()

class BigfootPostSerializer(serializers.ModelSerializer):
    image = serializers.CharField()
    owner = serializers.CharField()

    class Meta:
        model = BigfootPost
        fields = '__all__'

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

class UfoPostSerializer(serializers.ModelSerializer):
    image = serializers.CharField()
    owner = serializers.CharField()
    class Meta:
        model = UfoPost
        fields = '__all__'

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


class GhostPostSerializer(serializers.ModelSerializer):
    image = serializers.CharField()
    owner = serializers.CharField()
    class Meta:
        model = GhostPost
        fields = '__all__'

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


class OtherPostSerializer(serializers.ModelSerializer):
    image = serializers.CharField()
    owner = serializers.CharField()
    class Meta:
        model = OtherPost
        fields = '__all__'

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
