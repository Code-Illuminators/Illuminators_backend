"""Configuring the handler for requests."""
import requests
from posts.models import BigfootPost, UfoPost, GhostPost, OtherPost
from users.models import EntryPassword, User, Government, UserLoginIP
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from .models import Vote, VoteLog
from .serializers import VoteSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vote(request):
    """Create vote and votelog for all with role"""
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        vote = serializer.save()
        try:
            response=requests.post("http://go-voting:8080/voting/start", json=VoteSerializer(vote).data)
            if response.status_code == 200:
                if response.json().get("status") == "ok":
                    return Response({"message": "External service notified successfully",}, 
                                    VoteSerializer(vote).data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "External service have a problem. Responded with unexpected dats",}, 
                                    VoteSerializer(vote).data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"message": "External service returned error",
                                "status_code": response.status_code,}, 
                                    VoteSerializer(vote).data, status=status.HTTP_202_ACCEPTED)
        except requests.RequestException as e:
            return Response(
                {
                    "message": "Vote created, but failed to contact external service",
                },
                VoteSerializer(vote).data,
                status=status.HTTP_202_ACCEPTED,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def votes_list(request):
    """Get active votes list """
    user=request.user
    active_logs = VoteLog.objects.filter(user=user).select_related('vote')
    votes=[log.vote for log in active_logs]
    serializer=VoteSerializer(votes, many = True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def collect_vote(request, pk):
    """Collect voting data to update information"""
    try:
        vote = Vote.objects.get(pk=pk)
    except Vote.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        vote_log=VoteLog.objects.get(vote=vote, user=request.user, status=False)
    except VoteLog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    choice = request.data.get('choice')
    if choice not in ['for', 'against']:
        return Response({'error': 'choice must be "for" or "against"'}, status=status.HTTP_400_BAD_REQUEST)
    if choice=='for':
        vote_log.is_for=True
        vote.for_amount +=1
    else:
        vote_log.is_against=True
        vote.against_amount+=1
    vote_log.status=True
    vote_log.save()
    vote.save()
    vote.update_progress()
    return Response({
        'success': True,
        'vote_id': vote.id,
        'for_amount': vote.for_amount,
        'against_amount': vote.against_amount,
        'progress': round(vote.progress, 1)
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_vote(request, pk):
    """Delete voice and all related information"""
    try:
        vote = Vote.objects.get(pk=pk)
    except Vote.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    vote.delete()
    return Response({"message": "Vote and all logs deleted successfully"},
        status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all(request):
    """Delete all posts, reset users' password, and entry passwords."""
    if request.user.role != 'gold':
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    BigfootPost.objects.all().delete()
    UfoPost.objects.all().delete()
    GhostPost.objects.all().delete()
    OtherPost.objects.all().delete()
    EntryPassword.objects.all().delete()
    Government.objects.all().delete()

    for user in User.objects.all():
        temp_pass = get_random_string(length=10)
        user.password = make_password(temp_pass)
        user.force_password_change = True
        user.save(update_fields=['password', 'force_password_change'])

    return Response({'success': 'All data deleted and passwords reset'}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user_account(request, username):
    """Delete a user account and report IP to government."""
    try:
        user_to_delete = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    login_ips = UserLoginIP.objects.filter(user=user_to_delete).values_list('ip_hash', flat=True)
    for ip in login_ips:
        government_ip = Government(ip_hash=ip, added_by=None)
        government_ip.save()

    user_to_delete.delete()

    return Response({'success': f'User {username} deleted and IP reported'}, status=status.HTTP_200_OK)

