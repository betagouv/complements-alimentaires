# Generated by Django 5.0.2 on 2024-03-22 11:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MagicLinkToken",
            fields=[
                ("created", models.DateTimeField(editable=False)),
                ("modified", models.DateTimeField(editable=False)),
                ("expiration", models.DateTimeField()),
                (
                    "key",
                    models.CharField(
                        editable=False,
                        max_length=512,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "usage",
                    models.CharField(
                        choices=[("verify-email-address", "Verify email address")],
                        max_length=1024,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="magiclink_tokens",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
