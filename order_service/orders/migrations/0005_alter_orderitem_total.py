# Generated by Django 5.1.1 on 2025-01-20 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_alter_orderitem_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="total",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
