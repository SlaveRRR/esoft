# Generated by Django 4.2.5 on 2023-11-15 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_remove_realestate_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='city',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
