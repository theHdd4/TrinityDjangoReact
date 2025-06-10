from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Tenant(models.Model):
    name = models.CharField(max_length=255, unique=True)
    schema_name = models.CharField(max_length=255, unique=True)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Domain(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='domains'
    )
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.domain