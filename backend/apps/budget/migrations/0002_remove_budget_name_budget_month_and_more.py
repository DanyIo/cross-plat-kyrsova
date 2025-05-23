# Generated by Django 5.2 on 2025-04-15 15:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="budget",
            name="name",
        ),
        migrations.AddField(
            model_name="budget",
            name="month",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="budgetcategory",
            name="amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
