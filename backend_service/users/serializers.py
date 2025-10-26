"""Module for defining serializers related to user management and IP/password handling"""
import re
import ipaddress
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Government, EntryPassword

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for creating and viewing User instances."""
    class Meta:
        """Metadata for UserSerializer."""
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create a User instance with a hashed password."""
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing User instances."""
    class Meta:
        """Metadata for UserUpdateSerializer."""
        model = User
        fields = ['username', 'email', 'role']

    def update(self, instance, validated_data):
        """Update User instance with validated data."""
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance

class EntryPasswordCheckSerializer(serializers.Serializer):
    """Serializer for checking entry password access."""
    password = serializers.CharField(write_only=True, max_length=128)
    def validate_password(self, value):
        """Validate the provided password against the stored hash."""
        try:
            entry_password = EntryPassword.objects.last()
            if not entry_password.check_password(value):
                raise serializers.ValidationError("Invalid password!")
            return value
        except EntryPassword.DoesNotExist:
            raise serializers.ValidationError("Password is not set!")

class EntryPasswordSerializer(serializers.ModelSerializer):
    """Serializer for set entry password."""
    password = serializers.CharField(write_only=True, max_length=128)
    class Meta:
        """Metadata for EntryPasswordSerializer."""
        model = EntryPassword
        fields = ['password']

    def create(self, value):
        """Create an EntryPassword instance with a hashed password."""
        password = value.pop('password')
        entry_password = EntryPassword()
        entry_password.set_password(password)
        entry_password.save()
        return entry_password

class GovernmentSerializer(serializers.ModelSerializer):
    """Serializer for creating and validating Government instances."""
    ip_address = serializers.CharField(write_only=True)
    class Meta:
        """Metadata for GovernmentSerializer."""
        model = Government
        fields = ['ip_address', 'added_by']

    def validate_ip_address(self, value):
        """Validate the format of the IP address."""
        try:
            ipaddress.ip_address(value)
        except ValueError:
            raise serializers.ValidationError("Invalid IP address format.")
        return value

    def create(self, validated_data):
        """Create a Government instance with a hashed IP address."""
        ip_address = validated_data.pop('ip_address')
        government_ip = Government(added_by=validated_data['added_by'])
        government_ip.set_ip(ip_address)
        government_ip.save()
        return government_ip
