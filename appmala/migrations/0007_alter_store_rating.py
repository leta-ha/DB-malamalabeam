# Generated by Django 3.2.9 on 2021-12-17 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appmala', '0006_alter_store_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='rating',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
