# Generated by Django 4.1 on 2022-08-10 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_postimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image_path',
            field=models.ImageField(upload_to='posts/image'),
        ),
    ]
