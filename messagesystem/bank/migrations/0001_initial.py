# Generated by Django 4.1.2 on 2022-10-29 09:56

import bank.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                ("account_number", models.AutoField(primary_key=True, serialize=False)),
                (
                    "balance",
                    models.IntegerField(
                        validators=[bank.models.nonNegativeNumberValidator]
                    ),
                ),
                ("status", models.CharField(max_length=20)),
                ("description", models.CharField(max_length=30)),
                ("opened_on", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("cif", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                ("rmn", models.CharField(max_length=10)),
                ("email", models.EmailField(max_length=254)),
                ("joined_on", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Ledger",
            fields=[
                ("txid", models.AutoField(primary_key=True, serialize=False)),
                (
                    "amount",
                    models.IntegerField(
                        validators=[bank.models.nonNegativeNumberValidator]
                    ),
                ),
                ("time_stamp", models.DateTimeField(auto_now_add=True)),
                (
                    "reciever",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="reciever",
                        to="bank.account",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="sender",
                        to="bank.account",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="account",
            name="cif_fk",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="bank.customer"
            ),
        ),
    ]