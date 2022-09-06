# Generated by Django 4.1 on 2022-09-05 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0016_businesstype_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adcomment',
            name='ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adcomment', to='commerce.ad'),
        ),
        migrations.AlterField(
            model_name='adlike',
            name='ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adlike', to='commerce.ad'),
        ),
    ]
