"""Module for defining serializers related to moderation management"""
from rest_framework import serializers
from .models import VoteLog, Vote
from users.models import User

class VoteSerializer(serializers.ModelSerializer):
    """Serializer for Vote model."""
    nominated_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )
    nominated_user_username = serializers.ReadOnlyField(source='nominated_user.username')
    roles_allowed_vote = serializers.ListField(
        child=serializers.ChoiceField(choices=Vote.ROLE_ACCESS),
        write_only=True
    )
    for_amount = serializers.IntegerField(read_only=True)
    against_amount = serializers.IntegerField(read_only=True)
    progress = serializers.FloatField(read_only=True)
    class Meta:
        """Metadata for VoteSerializer."""
        model = Vote
        fields = ['id', 'nominated_user', 'nominated_user_username', 'roles_allowed_vote', 'for_amount', 'against_amount', 'progress']
    def create(self, validated_data):
        """Create a Vote instance with validated data."""
        roles = validated_data.pop('roles_allowed_vote', [])
        vote = Vote.objects.create(**validated_data, roles_allowed_vote=roles)
        
        users = User.objects.filter(role__in=roles)
        for user in users:
            VoteLog.objects.create(vote=vote, user=user)
        vote.update_progress()
        return vote

class VoteLogSerializer(serializers.ModelSerializer):
    """Serializer for VoteLog model."""
    vode_id = serializers.ReadOnlyField(source='vode.id')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        """Metadata for VoteLogSerializer."""
        model = VoteLog
        fields = ['id', 'vode', 'user', 'is_for', 'is_against', 'status']
    def create(self, validated_data):
        """Create a VoteLog instance."""
        return VoteLog.objects.create(**validated_data)
