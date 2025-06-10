from rest_framework import viewsets, permissions
from .models import Tenant, Domain
from .serializers import TenantSerializer, DomainSerializer


class TenantViewSet(viewsets.ModelViewSet):
    """
    Manage tenants (schemas). Admin-only for writes; all authenticated may list/retrieve.
    """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class DomainViewSet(viewsets.ModelViewSet):
    """
    Manage domain mappings for tenants. Admin-only for writes; authenticated users may list/retrieve.
    """
    queryset = Domain.objects.select_related("tenant").all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return super().get_permissions()
