# Generated by Django 3.2.9 on 2022-02-16 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='created',
        ),
    ]