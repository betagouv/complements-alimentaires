from django.contrib import admin

from .models import MagicLinkToken


@admin.register(MagicLinkToken)
class MagicLinkTokenAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "expiration",
        "key",
        "usage",
    )
    readonly_fields = ("key",)
    list_filter = ("expiration",)
    show_facets = admin.ShowFacets.NEVER
