# Generated by Django 5.0.3 on 2024-04-25 15:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_delete_userdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='userdata',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=15)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('profile_picture', models.ImageField(blank=True, default='media/default_profile_picture.jpg', null=True, upload_to='Media/Profiles/')),
                ('user_bio', models.TextField()),
                ('phone', models.IntegerField()),
                ('specialised', models.CharField(default=0, max_length=40)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]