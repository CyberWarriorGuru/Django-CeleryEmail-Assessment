# Generated by Django 4.2 on 2023-04-17 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_remove_connectedemail_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connectedemail",
            name="imap_host",
            field=models.CharField(max_length=200),
        ),
    ]