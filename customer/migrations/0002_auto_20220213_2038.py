# Generated by Django 3.2.9 on 2022-02-13 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="city",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="address",
            name="region",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
