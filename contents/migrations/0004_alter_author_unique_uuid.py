# Generated by Django 4.2.2 on 2024-02-03 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_author_avatar_url_delete_authoravatarurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='unique_uuid',
            field=models.CharField(max_length=255),
        ),
    ]