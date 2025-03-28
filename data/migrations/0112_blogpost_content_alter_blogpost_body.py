# Generated by Django 5.1.4 on 2025-01-07 15:28

import django_ckeditor_5.fields
import prose.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0111_alter_declaredingredient_request_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='content',
            field=prose.fields.RichTextField(blank=True, null=True, verbose_name='contenu'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='contenu (legacy)'),
        ),
    ]
