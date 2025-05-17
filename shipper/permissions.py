from rest_framework import permissions

class IsShipper(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and 
            request.user.role == 'shipper'
        )
    
    def has_object_permission(self, request, view, obj):
        # Ensure this matches your model field name (owner vs shipper)
        return obj.shipper == request.user  # Changed from obj.shipper to obj.owner