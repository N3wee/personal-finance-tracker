# Generated by Django 5.1.6 on 2025-02-21 16:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="date",
            field=models.DateField(),
        ),
    ]
