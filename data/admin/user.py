from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from data.models import DeclarantRole, SupervisorRole


class DeclarantRoleInline(admin.TabularInline):
    model = DeclarantRole
    fields = ("company",)
    readonly_fields = fields
    extra = 0
    can_delete = False


class SupervisorRoleInline(admin.TabularInline):
    model = SupervisorRole
    fields = ("company",)
    readonly_fields = fields
    extra = 0
    can_delete = False


@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "first_name", "last_name", "phone_number")}),
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "username",
    )

    inlines = (
        DeclarantRoleInline,
        SupervisorRoleInline,
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "is_verified",
                )
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
