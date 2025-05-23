# Generated by Django 5.2.1 on 2025-05-10 01:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Arranger",
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
                ("first_name", models.CharField(blank=True, max_length=100, null=True)),
                ("last_name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name_plural": "arrangers",
            },
        ),
        migrations.CreateModel(
            name="BorrowingOrganization",
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
                ("name", models.CharField(max_length=100)),
                ("contact_name", models.CharField(max_length=100)),
                ("contact_email", models.EmailField(blank=True, max_length=254)),
                ("contact_phone", models.CharField(blank=True, max_length=100)),
                ("notes", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Composer",
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
                ("first_name", models.CharField(blank=True, max_length=100, null=True)),
                ("last_name", models.CharField(max_length=100)),
                ("birth_year", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "verbose_name_plural": "composers",
            },
        ),
        migrations.CreateModel(
            name="Genre",
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
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name_plural": "genres",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="LoaningOrganization",
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
                ("name", models.CharField(max_length=100)),
                ("contact_name", models.CharField(max_length=100)),
                ("contact_email", models.EmailField(blank=True, max_length=254)),
                ("contact_phone", models.CharField(blank=True, max_length=100)),
                ("notes", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Publisher",
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
                ("name", models.CharField(max_length=100)),
                ("website", models.URLField(blank=True)),
            ],
            options={
                "verbose_name_plural": "publishers",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="RentalOrganization",
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
                ("name", models.CharField(max_length=100)),
                ("contact_name", models.CharField(max_length=100)),
                ("contact_email", models.EmailField(blank=True, max_length=254)),
                ("contact_phone", models.CharField(blank=True, max_length=100)),
                ("notes", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Piece",
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
                ("title", models.CharField(max_length=200)),
                (
                    "difficulty",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("EASY", "Easy"),
                            ("MOD_EASY", "Moderately Easy"),
                            ("MODERATE", "Moderate"),
                            ("MOD_DIFFICULT", "Moderately Difficult"),
                            ("DIFFICULT", "Difficult"),
                        ],
                        max_length=16,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("OWNED", "Owned"),
                            ("RENTED", "Rented"),
                            ("ON_LOAN", "On Loan"),
                            ("BORROWED", "Borrowed"),
                            ("ARCHIVED", "Archived"),
                        ],
                        default="OWNED",
                        max_length=10,
                    ),
                ),
                ("rental_start_date", models.DateField(blank=True, null=True)),
                ("rental_end_date", models.DateField(blank=True, null=True)),
                (
                    "rental_cost",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("loaning_start_date", models.DateField(blank=True, null=True)),
                ("loaning_end_date", models.DateField(blank=True, null=True)),
                ("borrowing_start_date", models.DateField(blank=True, null=True)),
                ("borrowing_end_date", models.DateField(blank=True, null=True)),
                ("copyright_date", models.DateField(blank=True, null=True)),
                ("purchase_date", models.DateField(blank=True, null=True)),
                ("location_drawer", models.CharField(blank=True, max_length=100)),
                ("location_number", models.CharField(blank=True, max_length=100)),
                ("notes", models.TextField(blank=True)),
                ("arranger", models.ManyToManyField(to="library.arranger")),
                (
                    "borrowing_organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="library.borrowingorganization",
                    ),
                ),
                ("composer", models.ManyToManyField(to="library.composer")),
                ("genre", models.ManyToManyField(blank=True, to="library.genre")),
                (
                    "loaning_organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="library.loaningorganization",
                    ),
                ),
                (
                    "publisher",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="library.publisher",
                    ),
                ),
                (
                    "rental_organization",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="library.rentalorganization",
                    ),
                ),
            ],
        ),
    ]
