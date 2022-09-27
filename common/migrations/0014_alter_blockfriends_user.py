# Generated by Django 4.1.1 on 2022-09-27 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0013_remove_blockfriends_user_blockfriends_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockfriends',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
