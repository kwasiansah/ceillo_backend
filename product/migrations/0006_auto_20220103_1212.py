# Generated by Django 3.2.9 on 2022-01-03 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_auto_20220102_1413"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="video",
            new_name="video_url",
        ),
        migrations.RenameField(
            model_name="productmedia",
            old_name="image",
            new_name="image_url",
        ),
        migrations.RemoveField(
            model_name="productmedia",
            name="main_image",
        ),
        migrations.RemoveField(
            model_name="product",
            name="category",
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="products",
                to="product.category",
            ),
        ),
        migrations.AlterField(
            model_name="productmedia",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="product.product",
            ),
        ),
    ]
