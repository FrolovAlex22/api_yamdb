# Generated by Django 3.2 on 2023-08-30 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='name',
            field=models.CharField(default=1, max_length=256, verbose_name='Жанр'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
