"""Configuring the handler for requests."""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .models import BigfootPost, UfoPost, GhostPost, OtherPost
from .serializers import BigfootPostSerializer, UfoPostSerializer
from .serializers import GhostPostSerializer, OtherPostSerializer

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_bigfoot(request):
    """Retrieve all Bigfoot posts ordered by creation date"""
    posts = BigfootPost.objects.all().order_by('-created_at')
    serializer = BigfootPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_bigfoot(request, user_id):
    """Retrieve Bigfoot posts for a specific user, ordered by creation date"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    posts = BigfootPost.objects.filter(owner=user).order_by('-created_at')
    serializer = BigfootPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_bigfoot(request):
    """Create a new Bigfoot post for the authenticated user"""
    serializer = BigfootPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_bigfoot(request, pk):
    """Update an existing Bigfoot post if the authenticated user is the owner"""
    try:
        post = BigfootPost.objects.get(pk=pk)
    except BigfootPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if post.owner != request.user:
        return Response({'error': 'Not authorized to edit this post'},
                    status=status.HTTP_403_FORBIDDEN)
    serializer = BigfootPostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_bigfoot(request, pk):
    """Delete a Bigfoot post if the authenticated user is the owner or has 'gold' role"""
    try:
        post = BigfootPost.objects.get(pk=pk)
    except BigfootPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if post.owner == request.user or request.user.role == 'gold':
        post.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Not authorized to delete this post'},
                status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_ufo(request):
    """Retrieve all ufo posts ordered by creation date"""
    posts = UfoPost.objects.all().order_by('-created_at')
    serializer = UfoPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_ufo(request, user_id):
    """Retrieve ufo posts for a specific user, ordered by creation date"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    posts = UfoPost.objects.filter(owner=user).order_by('-created_at')
    serializer = UfoPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ufo(request):
    """Create a new ufo post for the authenticated user"""
    serializer = UfoPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_ufo(request, pk):
    """Update an existing ufo post if the authenticated user is the owner"""
    try:
        post = UfoPost.objects.get(pk=pk)
    except UfoPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if post.owner != request.user:
        return Response({'error': 'Not authorized to edit this post'},
                    status=status.HTTP_403_FORBIDDEN)
    serializer = UfoPostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ufo(request, pk):
    """Delete a ufo post if the authenticated user is the owner or has 'gold' role"""
    try:
        post = UfoPost.objects.get(pk=pk)
    except UfoPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if post.owner == request.user or request.user.role == 'gold':
        post.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Not authorized to delete this post'},
                status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_ghosts(request):
    """Retrieve all Ghost posts ordered by creation date"""
    posts = GhostPost.objects.all().order_by('-created_at')
    serializer = GhostPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_ghosts(request, user_id):
    """Retrieve Ghost posts for a specific user, ordered by creation date"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    posts = GhostPost.objects.filter(owner=user).order_by('-created_at')
    serializer = GhostPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ghost(request):
    """Create a new Ghost post for the authenticated user"""
    serializer = GhostPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_ghost(request, pk):
    """Update an existing Ghost post if the authenticated user is the owner"""
    try:
        post = GhostPost.objects.get(pk=pk)
    except GhostPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if post.owner != request.user:
        return Response({'error': 'Not authorized to edit this post'},
                    status=status.HTTP_403_FORBIDDEN)
    serializer = GhostPostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ghost(request, pk):
    """Delete a Ghost post if the authenticated user is the owner or has 'gold' role"""
    try:
        post = GhostPost.objects.get(pk=pk)
    except GhostPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if post.owner == request.user or request.user.role == 'gold':
        post.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Not authorized to delete this post'},
                status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_others(request):
    """Retrieve all Other posts ordered by creation date"""
    posts = OtherPost.objects.all().order_by('-created_at')
    serializer = OtherPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_others(request, user_id):
    """Retrieve Other posts for a specific user, ordered by creation date"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    posts = OtherPost.objects.filter(owner=user).order_by('-created_at')
    serializer = OtherPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_other(request):
    """Create a new Other post for the authenticated user"""
    serializer = OtherPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_other(request, pk):
    """Update an existing Other post if the authenticated user is the owner"""
    try:
        post = OtherPost.objects.get(pk=pk)
    except OtherPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if post.owner != request.user:
        return Response({'error': 'Not authorized to edit this post'},
                    status=status.HTTP_403_FORBIDDEN)
    serializer = OtherPostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_other(request, pk):
    """Delete an Other post if the authenticated user is the owner or has 'gold' role"""
    try:
        post = OtherPost.objects.get(pk=pk)
    except OtherPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if post.owner == request.user or request.user.role == 'gold':
        post.delete()
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Not authorized to delete this post'},
                status=status.HTTP_403_FORBIDDEN)
