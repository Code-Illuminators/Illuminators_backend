import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import HunterIP

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for creating and viewing User instances."""
    class Meta:
        """Metadata for UserSerializer."""
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing User instances."""
    class Meta:
        """Metadata for UserUpdateSerializer."""
        model = User
        fields = ['username', 'email', 'role']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance

class HunterIPSerializer(serializers.ModelSerializer):
    """Serializer for creating and validating HunterIP instances."""
    ip_address = serializers.CharField(write_only=True)
    class Meta:
        model = HunterIP
        fields = ['ip_address', 'added_by']

    def validate_ip_address(self, value):
        ip_regex = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        if not re.match(ip_regex, value):
            raise serializers.ValidationError("Invalid IP address format.")
        return value

    def create(self, validated_data):
        ip_address = validated_data.pop('ip_address')
        hunter_ip = HunterIP(added_by=validated_data['added_by'])
        hunter_ip.set_ip(ip_address)
        hunter_ip.save()
        return hunter_ip
