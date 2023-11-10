# Generated by Django 4.2.7 on 2023-11-10 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0008_offers"),
    ]

    operations = [
        migrations.CreateModel(
            name="Demand",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("type", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("min_price", models.CharField(max_length=255)),
                ("max_price", models.CharField(max_length=255)),
                ("min_square", models.CharField(max_length=255)),
                ("max_square", models.CharField(max_length=255)),
                ("min_number_of_rooms", models.CharField(max_length=255, null=True)),
                ("max_number_of_rooms", models.CharField(max_length=255, null=True)),
                ("min_floor", models.CharField(max_length=255, null=True)),
                ("max_floor", models.CharField(max_length=255, null=True)),
                ("min_number_of_floors", models.CharField(max_length=255, null=True)),
                ("max_number_of_floors", models.CharField(max_length=255, null=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clientindemand",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "rieltor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rieltorindemand",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
