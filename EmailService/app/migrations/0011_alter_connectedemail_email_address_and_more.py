# Generated by Django 4.2 on 2023-04-17 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_alter_connectedemail_imap_port_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connectedemail",
            name="email_address",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="connectedemail",
            name="imap_password",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="connectedemail",
            name="imap_username",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="connectedemail",
            name="provider_name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="connectedemail",
            name="smtp_host",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="connectedemail",
            name="smtp_password",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="connectedemail",
            name="smtp_username",
            field=models.CharField(max_length=255),
        ),
    ]