# Generated by Django 4.1.1 on 2022-09-27 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0012_remove_blockfriends_user_blockfriends_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blockfriends',
            name='user',
        ),
        migrations.AddField(
            model_name='blockfriends',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='blocked_users', to='common.friends'),
            preserve_default=False,
        ),
    ]
