# Generated by Django 3.2 on 2023-09-03 07:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(message='Поле "slug" должно состоять из символов:[0-9a-zA-Z]', regex='^[0-9a-zA-Z]*$')], verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категория',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Titles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('year', models.IntegerField(verbose_name='Год выпуска')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='reviews.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Название',
                'verbose_name_plural': 'Названия',
            },
        ),
        migrations.CreateModel(
            name='TitlesGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.genre')),
                ('titles', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.titles')),
            ],
        ),
        migrations.AddField(
            model_name='titles',
            name='genre',
            field=models.ManyToManyField(through='reviews.TitlesGenre', to='reviews.Genre'),
        ),
    ]
