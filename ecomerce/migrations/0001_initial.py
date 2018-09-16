# Generated by Django 2.0.3 on 2018-09-04 03:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('image_url', models.CharField(default='null', max_length=250)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('image_url', models.CharField(default='null', max_length=250)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('item_category', models.CharField(max_length=140)),
                ('item_brand', models.CharField(max_length=140)),
                ('description', models.TextField()),
                ('image_url', models.CharField(default='null', max_length=250)),
                ('price', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100000), django.core.validators.MinValueValidator(0)])),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]