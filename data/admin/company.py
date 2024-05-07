from django.contrib import admin

from ..models.company import Company, DeclarantRole, SupervisorRole


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(SupervisorRole)
class SupervisorRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(DeclarantRole)
class DeclarantRoleAdmin(admin.ModelAdmin):
    pass
