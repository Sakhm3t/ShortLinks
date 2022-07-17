# Generated by Django 3.2.9 on 2022-07-17 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_link', models.TextField()),
                ('short_link', models.CharField(max_length=20, unique=True)),
                ('user_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]