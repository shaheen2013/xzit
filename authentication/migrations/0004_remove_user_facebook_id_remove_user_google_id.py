# Generated by Django 4.0.5 on 2022-06-20 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='facebook_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='google_id',
        ),
    ]
