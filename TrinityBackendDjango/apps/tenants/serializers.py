from rest_framework import serializers
from django.utils import timezone
from django_tenants.utils import schema_context
from django.core.management import call_command
from .models import Tenant, Domain
from apps.subscriptions.models import Company, SubscriptionPlan
from apps.config_store.models import TenantConfig
from apps.registry.models import App


class TenantSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(write_only=True, required=False)
    seats_allowed = serializers.IntegerField(write_only=True, required=False)
    project_cap = serializers.IntegerField(write_only=True, required=False)
    apps_allowed = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Tenant
        fields = [
            "id",
            "name",
            "schema_name",
            "created_on",
            "domain",
            "seats_allowed",
            "project_cap",
            "apps_allowed",
        ]
        read_only_fields = ["id", "created_on"]

    def create(self, validated_data):
        domain = validated_data.pop("domain", None)
        seats = validated_data.pop("seats_allowed", None)
        project_cap = validated_data.pop("project_cap", None)
        apps_allowed = validated_data.pop("apps_allowed", None)

        tenant = Tenant.objects.create(**validated_data)

        if domain:
            Domain.objects.create(domain=domain, tenant=tenant, is_primary=True)

        # Run migrations so tenant-specific tables exist
        call_command(
            "migrate_schemas",
            "--schema",
            tenant.schema_name,
            interactive=False,
            verbosity=0,
        )

        # Use the tenant schema for tenant-specific tables and default app seeds
        with schema_context(tenant.schema_name):
            # Seed default app templates if not already present
            default_apps = [
                ("Marketing Mix Modeling", "marketing-mix", "Preset: Pre-process + Build"),
                ("Forecasting Analysis", "forecasting", "Preset: Pre-process + Explore"),
                ("Promo Effectiveness", "promo-effectiveness", "Preset: Explore + Build"),
                ("Blank App", "blank", "Start from an empty canvas"),
            ]
            for name, slug, desc in default_apps:
                App.objects.get_or_create(slug=slug, defaults={"name": name, "description": desc})

            if seats is not None or project_cap is not None:
                company = Company.objects.create(tenant=tenant)
                SubscriptionPlan.objects.create(
                    company=company,
                    plan_name="Default",
                    seats_allowed=seats or 0,
                    project_cap=project_cap or 0,
                    renewal_date=timezone.now().date(),
                )

            if apps_allowed:
                TenantConfig.objects.create(
                    tenant=tenant, key="apps_allowed", value=apps_allowed
                )

        return tenant


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = [
            "id",
            "domain",
            "tenant",
            "is_primary",
        ]
        read_only_fields = ["id"]
