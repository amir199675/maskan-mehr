# Generated by Django 2.2.6 on 2019-11-03 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debt', '0002_add_damage_damage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='add_rent',
            name='pay_time',
            field=models.DateField(),
        ),
    ]
