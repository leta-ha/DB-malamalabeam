# Generated by Django 3.2.9 on 2021-12-17 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appmala', '0008_alter_store_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True),
        ),
    ]