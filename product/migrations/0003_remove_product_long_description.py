# Generated by Django 3.2.9 on 2021-12-31 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='long_description',
        ),
    ]
