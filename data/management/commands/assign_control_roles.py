from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from data.models import ControlRole, ControlRoleEmail


class Command(BaseCommand):
    help = "Assign control roles based on email list"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate without making changes",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        emails_in_list = ControlRoleEmail.objects.all().values_list("email", flat=True)
        emails_to_persist = ControlRole.objects.filter(always_persist=True, is_active=True).values_list(
            "user__email", flat=True
        )

        authorized_emails = emails_in_list.union(emails_to_persist)
        current_controllers = ControlRole.objects.filter(is_active=True).values_list("user__email", flat=True)

        emails_to_add = authorized_emails - current_controllers
        emails_to_remove = current_controllers - authorized_emails

        self.stdout.write(f"Emails to add: {len(emails_to_add)}")
        self.stdout.write(f"Emails to remove: {len(emails_to_remove)}")

        if dry_run:
            self.stdout.write("DRY RUN - No changes made")
            return

        # Ajout des nouveaux rôles de controle
        added_count = 0
        for email in emails_to_add:
            try:
                user = get_user_model.objects.get(email=email, is_active=True)
                ControlRole.objects.get_or_create(user=user)
                added_count += 1
                self.stdout.write(f"✓ Added control role to {email}")
            except get_user_model.DoesNotExist:
                # INFO : Éventuellement on pourrait envoyer des emails pour inviter ces usagers à créer un compte
                self.stdout.write(f"⚠ User not found for control role assignment: {email}")

        # Suppression des rôles de controle existants
        removed_count = 0
        for email in emails_to_remove:
            try:
                control_role = ControlRole.objects.get(user__email=email, is_active=True)
                control_role.delete()
                removed_count += 1
                self.stdout.write(f"✗ Removed control role from {email}")
            except ControlRole.DoesNotExist:
                pass

        self.stdout.write(self.style.SUCCESS(f"Successfully processed: {added_count} added, {removed_count} removed"))
