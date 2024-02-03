from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from contents.models import Author, Content

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@registry.register_document
class AuthorDocument(Document):

    info = fields.ObjectField(
        properties={
            "name": fields.TextField(),
            "platform": fields.TextField(),
        }
    )

    stats = fields.NestedField(
        properties={
            "follower_id": fields.IntegerField(),
            "follower_count": fields.IntegerField(),
        }
    )


    class Index:
        name = "author"

    class Django:
        model = Author

        fields = [
            "unique_id",
            "unique_uuid",
            "origin_unique_id",
            "username",
            "profile_text",
            "avatar_url",
        ]


@registry.register_document
class ContentDocument(Document):

    creation_info = fields.ObjectField(
        properties={
            "created_at": fields.TextField(),
            "timestamp": fields.TextField(),
        }
    )

    context = fields.ObjectField(
        properties={
            "main_text": fields.TextField(),
            "token_count": fields.IntegerField(),
            "char_count": fields.IntegerField(),
            "tag_count": fields.IntegerField(),
        }
    )
    
    stats = fields.ObjectField(
        properties={
            "likes_id": fields.TextField(),
            "likes_count": fields.TextField(),
            "views_id": fields.TextField(),
            "views_count": fields.IntegerField(),
            "comments_id": fields.IntegerField(),
            "comments_count": fields.IntegerField(),
        }
    )

    media = fields.ObjectField(
        properties={
            "media_type": fields.TextField(),
            "url": fields.TextField(),
        }
    )


    class Index:
        name = "content"

    class Django:
        model = Content

        fields = [
            "page_number",
            "author_unique_id",
            "author_username",
            "unique_id",
            "unique_uuid",
            "origin_unique_id",
        ]

@receiver(post_save, sender=Author)
def index_author(sender, instance, **kwargs):
    AuthorDocument().update(instance)

@receiver(post_delete, sender=Author)
def delete_author(sender, instance, **kwargs):
    AuthorDocument().update(instance, ignore=404)

@receiver(post_save, sender=Content)
def index_content(sender, instance, **kwargs):
    ContentDocument().update(instance)

@receiver(post_delete, sender=Content)
def delete_content(sender, instance, **kwargs):
    ContentDocument().update(instance, ignore=404)
