# Generated by Django 5.1.3 on 2025-07-28 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_book_author_summary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='favorite_books',
            new_name='wishlist_books',
        ),
    ]
