# Generated by Django 4.1.1 on 2023-09-25 23:53

from django.db import migrations, models
import django.db.models.deletion
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
                ("appointmentDate", models.DateTimeField(blank=True, null=True)),
                ("carType", models.CharField(max_length=50)),
                ("passengerAmount", models.PositiveIntegerField(default=2)),
                ("questNote", models.CharField(blank=True, max_length=100, null=True)),
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
        migrations.CreateModel(
            name="questProfile",
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
                ("quest_phone", models.CharField(max_length=10)),
                ("line_userId", models.CharField(blank=True, max_length=40, null=True)),
                (
                    "quest_linename",
                    models.CharField(blank=True, max_length=40, null=True),
                ),
                ("lineid", models.CharField(blank=True, max_length=120, null=True)),
                ("order_times", models.PositiveIntegerField(default=0)),
                ("total_cost", models.IntegerField(default=0)),
                (
                    "signUp_time",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={"ordering": ("-signUp_time",),},
        ),
        migrations.CreateModel(
            name="car_order",
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
                ("appointmentDate", models.DateTimeField(blank=True, null=True)),
                ("serviceType", models.CharField(max_length=20)),
                ("mileage", models.PositiveIntegerField(default=0)),
                ("total_cost", models.IntegerField(default=0)),
                ("is_pay", models.BooleanField(default=False)),
                (
                    "transaction_id",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("be_canceled", models.BooleanField(default=False)),
                (
                    "quest_phone",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="to_order",
                        to="hailAndChartered.questprofile",
                    ),
                ),
            ],
            options={"ordering": ("-pub_datetime",),},
        ),
    ]
