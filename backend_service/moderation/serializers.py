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
    vote_type = serializers.CharField()
    promotion_role = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    for_amount = serializers.IntegerField(read_only=True)
    against_amount = serializers.IntegerField(read_only=True)
    progress = serializers.FloatField(read_only=True)
    class Meta:
        """Metadata for VoteSerializer."""
        model = Vote
        fields = ['id', 'nominated_user', 'nominated_user_username', 'roles_allowed_vote', 'vote_type', 'promotion_role', 'for_amount', 'against_amount', 'progress']
    def validate(self, data):
        """Validate vote creation"""
        vote_type = data.get('vote_type')
        promotion_role = data.get('promotion_role')
        if not vote_type:
            raise serializers.ValidationError({"vote_type": "Vote type is required."})
        if vote_type not in ['promotion', 'excommunication']:
            raise serializers.ValidationError({"vote_type": "Invalid vote type."})
        if vote_type == 'promotion' and not promotion_role:
            raise serializers.ValidationError({"promotion_role": "This field is required for promotion votes."})
        return super().validate(data)
    
    def create(self, validated_data):
        """Create a Vote instance with validated data."""
        roles = validated_data.pop('roles_allowed_vote', [])
        nominated_user = validated_data.get('nominated_user')
        vote = Vote.objects.create(**validated_data, roles_allowed_vote=roles)
        users = User.objects.filter(role__in=roles)
        for user in users:
            if user != nominated_user:
                VoteLog.objects.create(vote=vote, user=user)
        vote.update_progress()
        return vote

class VoteLogSerializer(serializers.ModelSerializer):
    """Serializer for VoteLog model."""
    vote_id = serializers.ReadOnlyField(source='vote.id')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        """Metadata for VoteLogSerializer."""
        model = VoteLog
        fields = ['id', 'vote', 'user', 'is_for', 'is_against', 'status']
    def create(self, validated_data):
        """Create a VoteLog instance."""
        return VoteLog.objects.create(**validated_data)
