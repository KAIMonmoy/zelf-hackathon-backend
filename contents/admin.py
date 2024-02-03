from django.contrib import admin

from .models import (
    AuthorInfo,
    AuthorStats,
    Author,
    Content,
    ContentContext,
    ContentCreationInfo,
    ContentMedia,
    ContentOriginDetails,
    ContentStats,
    ContentApiPageInfo,
    AuthorDetailsApiInfo,
)


admin.site.register(AuthorInfo)
admin.site.register(AuthorStats)
admin.site.register(Author)

admin.site.register(Content)
admin.site.register(ContentContext)
admin.site.register(ContentCreationInfo)
admin.site.register(ContentMedia)
admin.site.register(ContentOriginDetails)
admin.site.register(ContentStats)

admin.site.register(ContentApiPageInfo)
admin.site.register(AuthorDetailsApiInfo)
