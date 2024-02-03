from django.db import models


# ===============================
# Author Models
# ===============================
class AuthorInfo(models.Model):
    name = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)


class Author(models.Model):
    unique_id = models.IntegerField(unique=True)
    unique_uuid = models.CharField(max_length=255)
    origin_unique_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    profile_text = models.TextField()
    info = models.OneToOneField(AuthorInfo, on_delete=models.CASCADE)
    avatar_url = models.URLField(null=True)

    def __str__(self) -> str:
        return self.username


class AuthorStats(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='stats')
    follower_id = models.IntegerField()
    follower_count = models.IntegerField()


# ===============================
# Content Models
# ===============================

class ContentCreationInfo(models.Model):
    created_at = models.DateTimeField()
    timestamp = models.DateTimeField()


class ContentContext(models.Model):
    main_text = models.CharField(max_length=255)
    token_count = models.IntegerField()
    char_count = models.IntegerField()
    tag_count = models.IntegerField()


class ContentOriginDetails(models.Model):
    origin_platform = models.CharField(max_length=255)
    origin_url = models.URLField(null=True)


class ContentMedia(models.Model):
    media_type_choices = (
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('AUDIO', 'Audio'),
    )
    media_type = models.CharField(max_length=255, choices=media_type_choices)
    url = models.URLField(null=True)


class ContentStats(models.Model):
    likes_id = models.IntegerField()
    likes_count = models.IntegerField()
    views_id = models.IntegerField()
    views_count = models.IntegerField()
    comments_id = models.IntegerField()
    comments_count = models.IntegerField()


class Content(models.Model):
    page_number = models.PositiveIntegerField()
    author_unique_id = models.CharField(max_length=255)
    author_username = models.CharField(max_length=255)
    unique_id = models.IntegerField(unique=True)
    unique_uuid = models.UUIDField()
    origin_unique_id = models.CharField(max_length=255)
    creation_info = models.OneToOneField(
        ContentCreationInfo, on_delete=models.CASCADE)
    context = models.OneToOneField(ContentContext, on_delete=models.CASCADE)
    origin_details = models.OneToOneField(
        ContentOriginDetails, on_delete=models.CASCADE)
    media = models.OneToOneField(ContentMedia, on_delete=models.CASCADE)
    stats = models.OneToOneField(ContentStats, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.page_number) + ' - ' + self.author_username + ' - ' + str(self.unique_id)


# ===============================
# 3rd Party API Models
# ===============================

class ContentApiPageInfo(models.Model):
    page_number = models.PositiveIntegerField(unique=True)
    contents_read = models.PositiveSmallIntegerField(default=0)
    page_status_choices = (
        ('READY', 'Ready'),
        ('IN_PROGRESS', 'In Progress'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('INCOMPLETE', 'Incomplete'),
    )
    page_status = models.CharField(max_length=255, choices=page_status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.page_number) + ' - ' + self.page_status


class AuthorDetailsApiInfo(models.Model):
    author_unique_id = models.CharField(max_length=255, unique=True)
    status_choices = (
        ('READY', 'Ready'),
        ('IN_PROGRESS', 'In Progress'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    )
    status = models.CharField(
        max_length=255, choices=status_choices, default='READY')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.author_unique_id) + ' - ' + self.status
