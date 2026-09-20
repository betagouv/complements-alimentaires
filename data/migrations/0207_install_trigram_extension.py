from django.db import migrations
import django.contrib.postgres.operations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0206_alter_company_country_and_more"),
    ]

    operations = [
        django.contrib.postgres.operations.TrigramExtension(),
    ]
