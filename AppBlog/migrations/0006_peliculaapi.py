# Generated by Django 4.1.7 on 2023-03-06 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("AppBlog", "0005_remove_pelicula_puntacion"),
    ]

    operations = [
        migrations.CreateModel(
            name="PeliculaAPI",
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
                ("titulo", models.CharField(max_length=255)),
                ("sinopsis", models.TextField()),
                ("poster", models.URLField()),
                ("fecha_lanzamiento", models.DateField()),
            ],
        ),
    ]