# Generated by Django 5.1.5 on 2025-01-24 16:59

import django.db.models.functions.comparison
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0117_remove_blogpost_body'),
    ]

    operations = [
        migrations.RenameField(
            model_name='declaration',
            old_name='overriden_article',
            new_name='overridden_article',
        ),
        migrations.RenameField(
            model_name='historicaldeclaration',
            old_name='overriden_article',
            new_name='overridden_article',
        ),
        # ValueError: Modifying GeneratedFields is not supported - the field data.Declaration.article must be removed and re-added with the new definition.
        migrations.RemoveField(
            model_name="declaration",
            name="article",
        ),
        migrations.RemoveField(
            model_name="historicaldeclaration",
            name="article",
        ),
        migrations.AddField(
            model_name='declaration',
            name='article',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.functions.comparison.Coalesce(models.Case(models.When(overridden_article='', then=models.Value(None)), default='overridden_article'), models.Case(models.When(calculated_article='', then=models.Value(None)), default='calculated_article'), models.Value(None)), output_field=models.TextField(null=True, verbose_name='article')),
        ),
        migrations.AddField(
            model_name='historicaldeclaration',
            name='article',
            field=models.GeneratedField(db_persist=True, expression=django.db.models.functions.comparison.Coalesce(models.Case(models.When(overridden_article='', then=models.Value(None)), default='overridden_article'), models.Case(models.When(calculated_article='', then=models.Value(None)), default='calculated_article'), models.Value(None)), output_field=models.TextField(null=True, verbose_name='article')),
        ),
    ]
