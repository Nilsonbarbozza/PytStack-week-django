# Generated by Django 5.1.7 on 2025-04-07 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorados', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentorados',
            name='token',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
    ]
