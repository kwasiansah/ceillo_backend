# Generated by Django 3.2.9 on 2021-11-23 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_auto_20211122_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='key',
            field=models.CharField(db_index=True, editable=False, max_length=40, unique=True, verbose_name='Key'),
        ),
    ]
