# Generated by Django 4.1 on 2022-09-09 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0023_reservation_num_of_guest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='num_of_guest',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
    ]
