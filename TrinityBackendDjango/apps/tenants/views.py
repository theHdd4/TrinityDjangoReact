from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.accounts.views import CsrfExemptSessionAuthentication
from .models import Tenant, Domain
from .serializers import TenantSerializer, DomainSerializer


@method_decorator(csrf_exempt, name="dispatch")
class TenantViewSet(viewsets.ModelViewSet):
    """
    Manage tenants (schemas). Admin-only for writes; all authenticated may list/retrieve.
    """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def create(self, request, *args, **kwargs):
        print("TenantViewSet.create called with", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Tenant validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print("Tenant data validated, saving…")
        try:
            self.perform_create(serializer)
            print("Tenant instance created successfully")
        except Exception as exc:
            print("Tenant creation failed during perform_create:", exc)
            raise
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        print("TenantViewSet.perform_create start")
        instance = serializer.save()
        print("TenantViewSet.perform_create saved", instance)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return super().get_permissions()


@method_decorator(csrf_exempt, name="dispatch")
class DomainViewSet(viewsets.ModelViewSet):
    """
    Manage domain mappings for tenants. Admin-only for writes; authenticated users may list/retrieve.
    """
    queryset = Domain.objects.select_related("tenant").all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def create(self, request, *args, **kwargs):
        print("DomainViewSet.create called with", request.data)
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAdminUser()]
        return super().get_permissions()
