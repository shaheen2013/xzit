# Generated by Django 4.0.6 on 2022-09-13 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_alter_country_country_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='country_name',
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
