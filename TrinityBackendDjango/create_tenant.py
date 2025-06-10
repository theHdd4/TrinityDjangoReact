#!/usr/bin/env python3
import os
import django
from django.core.management import call_command
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# Adjust this import path if your app label is different:
from apps.tenants.models import Tenant, Domain

def main():
    tenant_name = "acme_corp"
    tenant_schema = "acme_corp_schema"
    primary_domain = "acme.example.com"

    print("\n→ 1) Applying SHARED (public) migrations…")
    # Run only shared apps into the public schema
    call_command("migrate_schemas", "--shared", interactive=False, verbosity=1)
    print("   ✅ Shared migrations complete.\n")

    with transaction.atomic():
        # 2a) Create (or get) the Tenant row in public
        tenant_obj, created = Tenant.objects.get_or_create(
            schema_name=tenant_schema,
            defaults={"name": tenant_name, "auto_create_schema": True},
        )
        if created:
            print(f"→ 2) Created Tenant: {tenant_obj}")
        else:
            print(f"→ 2) Tenant already existed: {tenant_obj}")

        # 2b) Create its primary Domain in public
        domain_obj, domain_created = Domain.objects.get_or_create(
            domain=primary_domain,
            tenant=tenant_obj,
            defaults={"is_primary": True},
        )
        if domain_created:
            print(f"   → Created Domain: {domain_obj}")
        else:
            print(f"   → Domain already existed: {domain_obj}")
    print()

    print(f"→ 3) Running TENANT-SCHEMA migrations for '{tenant_schema}'…")
    # This will switch into acme_corp_schema and apply all TENANT_APPS there
    call_command("migrate_schemas", "--tenant", tenant_schema, interactive=False, verbosity=1)
    print("   ✅ Tenant-schema migrations complete.\n")

    print("All done! Tenant and all tables created.\n")

if __name__ == "__main__":
    main()
