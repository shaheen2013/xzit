# Generated by Django 4.1.1 on 2022-09-16 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0030_ad_business_hour_adinvitation_invite_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='business_hour',
        ),
        migrations.CreateModel(
            name='AdBusinessHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(blank=True, max_length=100, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ad_business_hour', to='commerce.ad')),
            ],
        ),
    ]
