# Generated by Django 5.0.7 on 2024-08-23 20:58

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_answer_userquestionnaireresponse_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionnaire',
            old_name='user',
            new_name='create_by',
        ),
        migrations.AddField(
            model_name='userquestionnaireresponse',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='questionnaire_response', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
