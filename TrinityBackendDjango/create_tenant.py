#!/usr/bin/env python3
import os
import django
from django.core.management import call_command
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.tenants.models import Tenant, Domain
from django.contrib.auth import get_user_model


def main():
    tenant_name = "acme_corp"
    tenant_schema = "acme_corp_schema"
    primary_domain = os.getenv("PRIMARY_DOMAIN", "localhost")

    print("\n→ Applying shared migrations…")
    call_command("migrate_schemas", "--shared", interactive=False, verbosity=0)

    User = get_user_model()
    if not User.objects.filter(username="harsha").exists():
        User.objects.create_superuser(username="harsha", password="harsha", email="")
        print("Created default admin 'harsha'")

    with transaction.atomic():
        tenant, _ = Tenant.objects.get_or_create(
            schema_name=tenant_schema,
            defaults={"name": tenant_name},
        )
        # ensure schema auto-creation is enabled then save
        tenant.auto_create_schema = True
        tenant.save()

        Domain.objects.get_or_create(domain=primary_domain, tenant=tenant, defaults={"is_primary": True})

    print("\n→ Applying tenant migrations…")
    call_command("migrate_schemas", "--schema", tenant_schema, interactive=False, verbosity=0)
    print("Tenant setup complete.")


if __name__ == "__main__":
    main()
