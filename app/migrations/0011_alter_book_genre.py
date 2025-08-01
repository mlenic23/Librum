# Generated by Django 5.1.3 on 2025-04-11 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_book_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('fantasy', 'Fantasy'), ('sci-fi', 'Sci-Fi'), ('romance', 'Romance'), ('mystery', 'Mystery'), ('history', 'History'), ('drama', 'Drama'), ('thriller', 'Thriller'), ('religion', 'Religion'), ('crime', 'Crime'), ('action', 'Action'), ('humor', 'Humor'), ('adventure', 'Adventure'), ('autobiography', 'Autobiography'), ('cookbook', 'Cookbook'), ('psychology', 'Psychology'), ('other', 'Other')], max_length=50),
        ),
    ]
