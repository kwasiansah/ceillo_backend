# Generated by Django 3.2.9 on 2021-12-16 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_alter_customer_agreed_to_terms'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='verified_email',
            field=models.BooleanField(default=True),
        ),
    ]
