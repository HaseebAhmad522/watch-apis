# Generated by Django 4.2.7 on 2023-11-02 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Watch",
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
                ("title", models.CharField(max_length=100)),
                ("price", models.FloatField()),
                ("description", models.TextField()),
                ("brand", models.CharField(max_length=100)),
                ("gender", models.CharField(max_length=100)),
                ("year", models.IntegerField()),
                ("condition", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="")),
                ("listing_code", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
                ("reference_number", models.CharField(max_length=100)),
                ("dealer_product_code", models.CharField(max_length=100)),
                ("movement", models.CharField(max_length=100)),
                ("movement_caliber", models.CharField(max_length=100)),
                ("frequency", models.CharField(max_length=100)),
                ("year_of_production", models.IntegerField()),
                ("scope_of_delivery", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=100)),
                ("lug_width", models.CharField(max_length=100)),
                ("power_reserve", models.CharField(max_length=100)),
                ("water_resistance", models.CharField(max_length=100)),
                ("bracelet_color", models.CharField(max_length=100)),
                ("availability", models.CharField(max_length=100)),
                ("base_caliber", models.CharField(max_length=100)),
                ("case_material", models.CharField(max_length=100)),
                ("bezel_material", models.CharField(max_length=100)),
                ("bracelet_material", models.CharField(max_length=100)),
                ("case_diameter", models.CharField(max_length=100)),
                ("thickness", models.CharField(max_length=100)),
                ("crystal", models.CharField(max_length=100)),
                ("dial", models.CharField(max_length=100)),
                ("clasp", models.CharField(max_length=100)),
                ("clasp_material", models.CharField(max_length=100)),
                ("number_of_jewels", models.CharField(max_length=100)),
                ("dial_numerals", models.CharField(max_length=100)),
                ("functions", models.TextField()),
            ],
        ),
    ]
