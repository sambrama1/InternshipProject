# Generated by Django 4.2.4 on 2023-09-06 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishes',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
