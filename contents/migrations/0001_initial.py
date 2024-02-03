# Generated by Django 4.2.2 on 2024-02-03 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.IntegerField(unique=True)),
                ('unique_uuid', models.UUIDField()),
                ('origin_unique_id', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('profile_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AuthorInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('platform', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ContentApiPageInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.PositiveIntegerField(unique=True)),
                ('contents_read', models.PositiveSmallIntegerField(default=0)),
                ('page_status', models.CharField(choices=[('READY', 'Ready'), ('IN_PROGRESS', 'In Progress'), ('SUCCESS', 'Success'), ('FAILED', 'Failed'), ('INCOMPLETE', 'Incomplete')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentContext',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_text', models.CharField(max_length=255)),
                ('token_count', models.IntegerField()),
                ('char_count', models.IntegerField()),
                ('tag_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ContentCreationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ContentMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_type', models.CharField(choices=[('IMAGE', 'Image'), ('VIDEO', 'Video'), ('AUDIO', 'Audio')], max_length=255)),
                ('url', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentOriginDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_platform', models.CharField(max_length=255)),
                ('origin_url', models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes_id', models.IntegerField()),
                ('likes_count', models.IntegerField()),
                ('views_id', models.IntegerField()),
                ('views_count', models.IntegerField()),
                ('comments_id', models.IntegerField()),
                ('comments_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_number', models.PositiveIntegerField()),
                ('author_unique_id', models.CharField(max_length=255)),
                ('author_username', models.CharField(max_length=255)),
                ('unique_id', models.IntegerField()),
                ('unique_uuid', models.UUIDField()),
                ('origin_unique_id', models.CharField(max_length=255)),
                ('context', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contents.contentcontext')),
                ('creation_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contents.contentcreationinfo')),
                ('media', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contents.contentmedia')),
                ('origin_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contents.contentorigindetails')),
                ('stats', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contents.contentstats')),
            ],
        ),
        migrations.CreateModel(
            name='AuthorStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower_id', models.IntegerField()),
                ('follower_count', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='contents.author')),
            ],
        ),
        migrations.CreateModel(
            name='AuthorAvatarURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avatar_urls', to='contents.author')),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contents.authorinfo'),
        ),
    ]