# Generated by Django 5.1.1 on 2024-09-18 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Prediction", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="task",
            old_name="Quantite",
            new_name="Quantite",
        ),
    ]
