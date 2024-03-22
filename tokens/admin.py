from django.contrib import admin

from .models.magic_link_token import MagicLinkToken


@admin.register(MagicLinkToken)
class MagicLinkTokenAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "expiration",
        "key",
        "usage",
    )
    list_filter = ("expiration", "user")
