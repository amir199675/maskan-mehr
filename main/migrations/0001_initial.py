# Generated by Django 2.2.6 on 2019-10-28 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=128)),
                ('picture', models.ImageField(upload_to='slider-pic/')),
                ('status', models.CharField(choices=[('Public', 'public'), ('Draft', 'draft')], max_length=32)),
            ],
        ),
    ]
