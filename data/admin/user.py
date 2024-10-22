from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

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
    def __init__(self, model, admin_site):
        fieldsets = self.fieldsets[:1] + ((None, {"fields": ("is_verified", "phone_number")}),) + self.fieldsets[1:]
        self.fieldsets = fieldsets
        super().__init__(model, admin_site)

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
