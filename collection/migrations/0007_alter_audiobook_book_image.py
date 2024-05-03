# Generated by Django 5.0.4 on 2024-05-03 10:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collection", "0006_alter_audiobook_book_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="audiobook",
            name="book_image",
            field=models.ImageField(
                blank=True,
                default="books/audio-book.png",
                null=True,
                upload_to="books/",
            ),
        ),
    ]
