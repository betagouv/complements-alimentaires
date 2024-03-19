from django.contrib import admin
from ..models.company import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass
