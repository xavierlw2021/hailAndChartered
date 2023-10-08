# Generated by Django 4.1.1 on 2023-10-08 10:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="chartered_order",
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
                (
                    "pub_datetime",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("userId", models.CharField(blank=True, max_length=40, null=True)),
                ("appointmentDate", models.DateTimeField(blank=True, null=True)),
                ("carType", models.CharField(max_length=50)),
                ("passengerAmount", models.PositiveIntegerField(default=2)),
                ("chtd_time", models.CharField(max_length=30)),
                ("total_cost", models.IntegerField(default=0)),
                ("questNote", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "transaction_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("paid", models.BooleanField(default=False)),
            ],
            options={"ordering": ("-appointmentDate",),},
        ),
        migrations.CreateModel(
            name="charteredOption",
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
                ("carType", models.CharField(max_length=50)),
                ("carImgUrl", models.URLField(blank=True, null=True)),
                ("chtdStartPrice", models.PositiveIntegerField(default=3000)),
                ("chtdAlldayPrice", models.PositiveIntegerField(default=4500)),
                ("timeOutPrice", models.PositiveIntegerField(default=400)),
                ("onOff", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="hailOption",
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
                ("agencyName", models.CharField(max_length=50)),
                (
                    "agencyNumber",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("agencyUrl", models.URLField(blank=True, null=True)),
                ("imgUrl", models.URLField(blank=True, null=True)),
                ("onOff", models.BooleanField(default=True)),
            ],
        ),
    ]
