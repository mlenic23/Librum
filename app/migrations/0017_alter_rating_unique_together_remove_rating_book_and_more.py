# Generated by Django 5.1.3 on 2025-04-21 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_book_facts_book_summary_comment_rating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='rating',
            name='book',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.RemoveField(
            model_name='book',
            name='description',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
