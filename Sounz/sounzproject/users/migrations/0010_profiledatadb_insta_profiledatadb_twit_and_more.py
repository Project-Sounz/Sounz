# Generated by Django 5.0.3 on 2024-05-05 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_postdb_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledatadb',
            name='insta',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profiledatadb',
            name='twit',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profiledatadb',
            name='yout',
            field=models.URLField(blank=True, null=True),
        ),
    ]
