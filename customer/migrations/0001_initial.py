# Generated by Django 3.2.9 on 2022-02-13 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0006_require_contenttypes_0002"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[("ACTIVE", "Active"), ("REMOVED", "Removed")],
                        default="ACTIVE",
                        max_length=7,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=150,
                        verbose_name="first name",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="last name"),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                ("phone_number", models.CharField(max_length=10)),
                (
                    "photo",
                    models.ImageField(blank=True, null=True, upload_to="profile/"),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("agreed_to_terms", models.BooleanField(default=False)),
                (
                    "university",
                    models.CharField(
                        blank=True,
                        choices=[("KNUST", "Knust"), ("UG", "UG")],
                        max_length=5,
                    ),
                ),
                ("verified_email", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer",
                "verbose_name_plural": "Customers",
            },
        ),
        migrations.CreateModel(
            name="Merchant",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "brand",
                    models.CharField(
                        help_text="The merchant name you would want to use",
                        max_length=250,
                    ),
                ),
                ("id_card", models.ImageField(null=True, upload_to="merchant/")),
                (
                    "id_card_type",
                    models.CharField(
                        choices=[
                            ("National", "National"),
                            ("Driver", "Driver"),
                            ("Student", "Student"),
                            ("Voter", "Voter"),
                        ],
                        default="Student",
                        max_length=8,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "customer",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="merchant",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AuthToken",
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
                    "key",
                    models.CharField(
                        db_index=True,
                        editable=False,
                        max_length=40,
                        unique=True,
                        verbose_name="Key",
                    ),
                ),
                ("expire", models.DateTimeField()),
                ("type", models.CharField(default="", max_length=250)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_token",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="customer",
                    ),
                ),
            ],
            options={
                "verbose_name": "Token",
                "verbose_name_plural": "Tokens",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Address",
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
                ("hostel", models.CharField(blank=True, max_length=250, null=True)),
                ("room_number", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "customer",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
