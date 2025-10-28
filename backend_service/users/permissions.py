from rest_framework import permissions
from django.conf import settings

class InternalServiceAccess(permissions.BasePermission):
    """Custom permission to allow access only to internal services."""
    def has_permission(self, request, view):
        """Check if the request have access internal token."""
        auth_header = request.headers.get("X-Internal-Token")
        return auth_header == settings.INTERNAL_SERVICE_TOKEN