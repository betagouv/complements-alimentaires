from django.contrib import admin

from ..models.company import Company, DeclarantRole, SupervisorRole


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = (
        "social_name",
        "commercial_name",
        "vat",
        "siret",
    )


@admin.register(SupervisorRole)
class SupervisorRoleAdmin(admin.ModelAdmin):
    search_fields = (
        "user__first_name",
        "user__last_name",
        "company__social_name",
        "company__commercial_name",
    )


@admin.register(DeclarantRole)
class DeclarantRoleAdmin(admin.ModelAdmin):
    search_fields = (
        "user__first_name",
        "user__last_name",
        "company__social_name",
        "company__commercial_name",
    )
