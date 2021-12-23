# Generated by Django 3.2.9 on 2021-12-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productmedia",
            name="video",
            field=models.FileField(
                blank=True,
                default="default/defaultvid.mp4",
                null=True,
                upload_to="products/video/",
            ),
        ),
    ]
