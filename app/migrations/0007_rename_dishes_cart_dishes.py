# Generated by Django 4.2.4 on 2023-09-08 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_dishes_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='Dishes',
            new_name='dishes',
        ),
    ]