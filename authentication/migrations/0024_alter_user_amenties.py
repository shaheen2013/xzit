# Generated by Django 4.1 on 2022-08-26 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0023_amenities_remove_user_business_days_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='amenties',
            field=models.ManyToManyField(to='authentication.amenities'),
        ),
    ]
