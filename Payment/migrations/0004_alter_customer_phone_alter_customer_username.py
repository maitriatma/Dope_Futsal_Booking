# Generated by Django 5.0.6 on 2025-02-18 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
