from django.contrib import admin

from .models import MagicLinkToken, InseeToken


@admin.register(MagicLinkToken)
class MagicLinkTokenAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "expiration",
        "key",
        "usage",
    )
    readonly_fields = ("key",)
    list_filter = ("expiration", "user")


@admin.register(InseeToken)
class InseeTokenAdmin(admin.ModelAdmin):
    list_display = (
        "expiration",
        "key",
    )
    readonly_fields = ("key",)
    list_filter = ("expiration",)
