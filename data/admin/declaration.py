from django.contrib import admin
from data.models import Declaration


@admin.register(Declaration)
class DeclarationAdmin(admin.ModelAdmin):

    list_display = ("name", "status", "company", "author")
    list_filter = ("status", "company", "author")
