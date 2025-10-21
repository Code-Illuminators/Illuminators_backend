from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, UserUpdateSerializer, GovernmentSerializer
from .serializers import EntryPasswordCheckSerializer, EntryPasswordSerializer
from .models import EntryPassword

User = get_user_model()

@api_view(['POST'])
def check_entry_password(request):
    serializer = EntryPasswordCheckSerializer(data=request.data)
    if serializer.is_valid():
        return Response({'valid': True,'message': 'Succses!'}, status=status.HTTP_200_OK)
    return Response({'valid': False, 'message': 'Invalid password!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def set_entry_password(request):
    serializer = EntryPasswordSerializer(data=request.data)
    if serializer.is_valid():
        entry_password = serializer.save()
        return Response({'success': True,'message': 'New password is set!', 'password_id': entry_password.id}, status=status.HTTP_201_CREATED)  
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_entry_password(request, password_id):
    try:
        entry_password = EntryPassword.objects.get(id=password_id)
        entry_password.delete()
        return Response({'success': True, 'message': f'Password {password_id} deleted!'}, status=status.HTTP_200_OK)
    except EntryPassword.DoesNotExist:
        return Response({'error': 'This password is not here!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_active_password(request):
    try:
        entry_password = EntryPassword.objects.last()
        return Response({'active_password_id': entry_password.id, 'exists': True})
    except EntryPassword.DoesNotExist:
        return Response({'exists': False,'message': 'There is not active password'})

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def users_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    new_password = request.data.get('new_password')
    if not new_password:
        return Response({'error': 'New password required'}, status=status.HTTP_400_BAD_REQUEST)
    user.password = make_password(new_password)
    user.save()
    return Response({'success': 'Password changed successfully'})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_hunter_ip(request):
    serializer = GovernmentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(added_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

