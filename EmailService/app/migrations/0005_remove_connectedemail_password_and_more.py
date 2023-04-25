# Generated by Django 4.2 on 2023-04-16 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0004_campaign"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="connectedemail",
            name="password",
        ),
        migrations.AddField(
            model_name="connectedemail",
            name="access_token",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="connectedemail",
            name="client_id",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="connectedemail",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="connectedemail",
            name="refresh_token",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="connectedemail",
            name="secret_key",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="connectedemail",
            name="provider",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="connectedemail",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]