from django.db import migrations
import django.contrib.postgres.operations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0207_user_last_login_proconnect"),
    ]

    operations = [
        django.contrib.postgres.operations.TrigramExtension(),
    ]
