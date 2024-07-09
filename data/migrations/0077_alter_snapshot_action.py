# Generated by Django 5.0.6 on 2024-07-08 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0076_snapshot_action_snapshot_post_validation_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="snapshot",
            name="action",
            field=models.CharField(
                blank=True,
                choices=[
                    ("SUBMIT", "soumettre pour instruction"),
                    ("TAKE_FOR_INSTRUCTION", "prendre pour instruction"),
                    ("OBSERVE_NO_VISA", "mettre en observation sans visa"),
                    ("AUTHORIZE_NO_VISA", "autoriser sans visa"),
                    ("RESPOND_TO_OBSERVATION", "répondre à une observation"),
                    ("RESPOND_TO_OBJECTION", "répondre à une objection"),
                    ("REQUEST_VISA", "demander un visa"),
                    ("TAKE_FOR_VISA", "prendre pour visa"),
                    ("APPROVE_VISA", "valider le visa"),
                    ("REFUSE_VISA", "refuser le visa"),
                    ("WITHDRAW", "retirer du marché"),
                    ("ABANDON", "mettre en abandon"),
                    ("OTHER", "autre"),
                ],
                default="OTHER",
                max_length=50,
            ),
        ),
    ]