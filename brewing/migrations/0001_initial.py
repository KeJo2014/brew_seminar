# Generated by Django 4.1.3 on 2022-11-29 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="brew_recipe",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("date", models.DateField(auto_now=True)),
                ("bier_sorte", models.CharField(max_length=100)),
                ("author", models.CharField(max_length=100)),
                ("ausschlagwuerze", models.CharField(default="", max_length=100)),
                ("sudhausausbeute", models.CharField(max_length=100)),
                ("stamwuerze", models.CharField(max_length=100)),
                ("ibu", models.IntegerField()),
                ("ebc", models.IntegerField()),
                ("alcohol", models.FloatField(default=0)),
                ("description", models.TextField(max_length=1000)),
                ("brauwasser", models.CharField(max_length=800)),
                ("schuettung", models.CharField(max_length=800)),
                ("maischplan", models.CharField(max_length=800)),
                ("wuerzekochen", models.CharField(max_length=800)),
                ("gaerung", models.CharField(max_length=800)),
                ("phase", models.CharField(max_length=8000)),
                ("number_of_brews", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="messurement",
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
                ("time", models.DateTimeField(auto_now=True)),
                ("temperature", models.CharField(max_length=10)),
                ("plato", models.CharField(max_length=10)),
                ("engine", models.BooleanField(default=False)),
                ("step", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="recipe",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("date", models.DateField(auto_now=True)),
                ("bier_sorte", models.CharField(max_length=100)),
                ("author", models.CharField(max_length=100)),
                ("ausschlagwuerze", models.CharField(default="", max_length=100)),
                ("sudhausausbeute", models.CharField(max_length=100)),
                ("stamwuerze", models.CharField(max_length=100)),
                ("ibu", models.IntegerField()),
                ("ebc", models.IntegerField()),
                ("alcohol", models.FloatField(default=0)),
                ("description", models.TextField(max_length=1000)),
                ("brauwasser", models.CharField(max_length=800)),
                ("schuettung", models.CharField(max_length=800)),
                ("maischplan", models.CharField(max_length=800)),
                ("wuerzekochen", models.CharField(max_length=800)),
                ("gaerung", models.CharField(max_length=800)),
                ("phase", models.CharField(max_length=8000)),
            ],
        ),
    ]
