# Generated by Django 5.0.4 on 2024-04-23 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postdata',
            name='pid',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]