# Generated by Django 5.0.3 on 2024-04-24 13:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userdata_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]