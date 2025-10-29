from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

def get_all_posts(model, serializer_class):
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def view(request):
        posts = model.objects.all().order_by('-created_at')
        serializer = serializer_class(posts, many=True)
        return Response(serializer.data)
    return view

def get_user_posts(model, serializer_class):
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def view(request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        posts = model.objects.filter(owner=user).order_by('-created_at')
        serializer = serializer_class(posts, many=True)
        return Response(serializer.data)
    return view

def create_post(serializer_class):
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def view(request):
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return view

def update_post(model, serializer_class):
    @api_view(['PATCH'])
    @permission_classes([IsAuthenticated])
    def view(request, pk):
        try:
            post = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.owner != request.user:
            return Response({'error': 'Not authorized to edit this post'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializer_class(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return view

def delete_post(model):
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def view(request, pk):
        try:
            post = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.owner == request.user or request.user.role == 'gold':
            post.delete()
            return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Not authorized to delete this post'}, status=status.HTTP_403_FORBIDDEN)
    return view