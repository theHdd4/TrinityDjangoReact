from rest_framework import serializers
from django.core.management import call_command
from django.db import transaction
from .models import Tenant, Domain

class TenantSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(write_only=True)

    class Meta:
        model = Tenant
        fields = ["id", "name", "schema_name", "created_on", "domain"]
        read_only_fields = ["id", "created_on"]

    def create(self, validated_data):
        domain = validated_data.pop("domain")
        schema = validated_data.get("schema_name", "").lower().replace("-", "_").replace(" ", "_")
        validated_data["schema_name"] = schema
        with transaction.atomic():
            tenant = Tenant.objects.create(**validated_data)
            Domain.objects.create(domain=domain, tenant=tenant, is_primary=True)
        tenant.create_schema(check_if_exists=True)
        call_command("migrate_schemas", "--schema", tenant.schema_name, interactive=False, verbosity=0)
        return tenant

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ["id", "domain", "tenant", "is_primary"]
        read_only_fields = ["id"]
