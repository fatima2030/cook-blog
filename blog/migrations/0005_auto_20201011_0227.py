# Generated by Django 3.0.6 on 2020-10-11 09:27

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20201011_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.upload_location),
        ),
    ]
