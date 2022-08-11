# Generated by Django 4.1 on 2022-08-11 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0014_remove_ad_business_sub_type_ad_business_sub_type'),
        ('authentication', '0013_remove_user_business_sub_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='business_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_business_type', to='commerce.businesstype'),
        ),
    ]
