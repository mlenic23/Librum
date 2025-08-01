# Generated by Django 5.1.3 on 2025-04-11 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_book_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('fiction', 'Fiction'), ('fantasy', 'Fantasy'), ('sci-fi', 'Sci-Fi'), ('romance', 'Romance'), ('mystery', 'Mystery'), ('biography', 'Biography'), ('history', 'History')], default=111, max_length=50),
            preserve_default=False,
        ),
    ]
