# Generated by Django 4.0.5 on 2022-06-28 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_image',
            field=models.ImageField(null=True, upload_to='movies/images'),
        ),
    ]