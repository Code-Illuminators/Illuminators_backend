import json
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import BigfootPostSerializer, UfoPostSerializer, GhostPostSerializer, OtherPostSerializer
from posts.models import BigfootPost, UfoPost, GhostPost, OtherPost

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def backup_posts(request):
    """Create a JSON backup of all posts"""
    bigfoot = BigfootPost.objects.all()
    ufo = UfoPost.objects.all()
    ghost = GhostPost.objects.all()
    other = OtherPost.objects.all()
    data = {
        "bigfoot": BigfootPostSerializer(bigfoot, many=True).data,
        "ufo": UfoPostSerializer(ufo, many=True).data,
        "ghost": GhostPostSerializer(ghost, many=True).data,
        "other": OtherPostSerializer(other, many=True).data,
    }
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="posts_backup.json"'
    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restore_posts(request):
    """Restore posts from JSON payload"""
    try:
        data = request.data
        if not isinstance(data, dict):
            return Response(
                {"error": "Expected a dictionary  of records"},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception:
        return Response(
            {"error": "Invalid JSON"},
            status=status.HTTP_400_BAD_REQUEST
        )
    created_total = 0
    post_type = {
        "bigfoot": (BigfootPostSerializer, BigfootPost),
        "ufo": (UfoPostSerializer, UfoPost),
        "ghost": (GhostPostSerializer, GhostPost),
        "other": (OtherPostSerializer, OtherPost),
    }
    for key, (serializer_class, model_class) in post_type.items():
        posts_data = data.get(key, [])

        serializer = serializer_class(data=posts_data, many=True)
        if serializer.is_valid():
            serializer.save()
            created_total += len(posts_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"status": "Restore successful", "count": created_total}, status=status.HTTP_201_CREATED)