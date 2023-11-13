# Generated by Django 4.2.7 on 2023-11-12 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0010_demand_heading_offers_heading"),
    ]

    operations = [
        migrations.CreateModel(
            name="Deal",
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
                ("heading", models.CharField(default=1, max_length=255)),
                ("confirmed", models.CharField(max_length=2)),
                (
                    "demand_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="demandDeal",
                        to="mainapp.demand",
                    ),
                ),
                (
                    "offer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offerDeal",
                        to="mainapp.offers",
                    ),
                ),
            ],
        ),
    ]
