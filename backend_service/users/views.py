from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, UserUpdateSerializer, GovernmentSerializer
from .serializers import EntryPasswordCheckSerializer, EntryPasswordSerializer, LoginSerializer
from .models import EntryPassword
from .permissions import InternalServiceAccess
User = get_user_model()

@api_view(['POST'])
def check_entry_password(request):
    """Check if the provided entry password is valid"""
    serializer = EntryPasswordCheckSerializer(data=request.data)
    if serializer.is_valid():
        return Response({'valid': True,'message': 'Succses!'}, status=status.HTTP_200_OK)
    return Response({'valid': False, 'message': 'Invalid password!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([InternalServiceAccess])
def set_entry_password(request):
    """Set a new entry password"""
    serializer = EntryPasswordSerializer(data=request.data)
    if serializer.is_valid():
        entry_password = serializer.save()
        return Response({'success': True,'message': 'New password is set!', 'password_id': entry_password.id}, status=status.HTTP_201_CREATED)  
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([InternalServiceAccess])
def delete_entry_password(request, password_id):
    """Delete an entry password by its ID"""
    try:
        entry_password = EntryPassword.objects.get(id=password_id)
        entry_password.delete()
        return Response({'success': True, 'message': f'Password {password_id} deleted!'}, status=status.HTTP_200_OK)
    except EntryPassword.DoesNotExist:
        return Response({'error': 'This password is not here!'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([InternalServiceAccess])
def get_active_password(request):
    """Retrieve the ID of the most recently set entry password"""
    entry_password = EntryPassword.objects.last()
    if entry_password is None:
        return Response({'exists': False,'message': 'There is not active password'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'active_password_id': entry_password.id, 'exists': True}, status=status.HTTP_200_OK)        

@api_view(['POST'])
def register_user(request):
    """Register a new user"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated | InternalServiceAccess])
def users_list(request):
    """Retrieve a list of all users"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change the password for the authenticated user"""    
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
    """Update the profile of the authenticated user"""
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_government_ip(request):
    """Report a IP address by hashing and storing it"""
    serializer = GovernmentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(added_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    """Authenticate a user and return a token"""
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        return Response({
            'refresh': serializer.validated_data['refresh'],
            'access': serializer.validated_data['access'],
            'user': {
                'id': serializer.validated_data['user'].id,
                'username': serializer.validated_data['user'].username,
                'email': serializer.validated_data['user'].email,
                'role': serializer.validated_data['user'].role,
                'force_password_change': serializer.validated_data['user'].force_password_change,
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
