# Generated by Django 5.0.2 on 2024-03-22 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0031_alter_user_username"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_verified",
            field=models.BooleanField(default=False, verbose_name="Compte vérifié ?"),
        ),
    ]
