# Generated by Django 4.0.6 on 2022-08-08 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_user_is_verified_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
