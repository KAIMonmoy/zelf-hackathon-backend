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
import requests
from celery import shared_task

from .config import APIConfig

headers = {
    'content-type': 'application/json',
    'x-api-key': APIConfig.API_KEY,
}


@shared_task
def fetch_contents():
    api_page_info = ContentApiPageInfo.objects\
        .filter(page_status__in=['READY', 'FAILED', 'INCOMPLETE'])\
        .order_by('updated_at')\
        .first()

    if not api_page_info:
        print("No pages to fetch")
        return

    url = APIConfig.BASE_URL_V1 + '/contents?page=' + \
        str(api_page_info.page_number)
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
    except Exception as ex:
        print('Failed to fetch data. Error:', ex)
        return

    api_page_info.page_status = 'IN_PROGRESS'
    api_page_info.save()

    if response.status_code == 200:
        for record in data['data']:
            try:
                Content.objects.create(
                    unique_id=record['unique_id'],
                    unique_uuid=record['unique_uuid'],
                    origin_unique_id=record['origin_unique_id'],
                    page_number=api_page_info.page_number,
                    author_unique_id=record['author']['id'],
                    author_username=record['author']['username'],
                    creation_info=ContentCreationInfo.objects.create(
                        created_at=record['creation_info']['created_at'],
                        timestamp=record['creation_info']['timestamp'],
                    ),
                    context=ContentContext.objects.create(
                        main_text=record['context']['main_text'],
                        token_count=record['context']['token_count'],
                        char_count=record['context']['char_count'],
                        tag_count=record['context']['tag_count'],
                    ),
                    origin_details=ContentOriginDetails.objects.create(
                        origin_platform=record['origin_details']['origin_platform'],
                        origin_url=record['origin_details']['origin_url'],
                    ),
                    media=ContentMedia.objects.create(
                        media_type=record['media']['media_type'],
                        url=None if not record['media']['urls'] else record['media']['urls'][0],
                    ),
                    stats=ContentStats.objects.create(
                        likes_id=record['stats']['digg_counts']['likes']['id'],
                        likes_count=record['stats']['digg_counts']['likes']['count'],
                        views_id=record['stats']['digg_counts']['views']['id'],
                        views_count=record['stats']['digg_counts']['views']['count'],
                        comments_id=record['stats']['digg_counts']['comments']['id'],
                        comments_count=record['stats']['digg_counts']['comments']['count'],
                    )
                )
                AuthorDetailsApiInfo.objects.get_or_create(
                    author_unique_id=record['author']['id']
                )
            except Exception as ex:
                print('Failed to save record. Error:', ex)

        api_page_info.contents_read = data['page_size']
        api_page_info.page_status = 'SUCCESS' if data['page_size'] > APIConfig.MAX_PAGE_SIZE else 'INCOMPLETE'
        api_page_info.save()

        ContentApiPageInfo.objects.create(
            page_number=api_page_info.page_number + 1,
            page_status='READY'
        )
    else:
        api_page_info.page_status = 'FAILED'
        api_page_info.save()
        print("Failed to fetch data. Status code:", response.status_code)
        print(response.json())


@shared_task
def fetch_author_details():
    author_api_info = AuthorDetailsApiInfo.objects\
        .filter(status__in=['READY', 'FAILED'])\
        .order_by('updated_at')\
        .first()

    if not author_api_info:
        print("No authors to fetch")
        return

    url = APIConfig.BASE_URL_V1 + '/authors/' + \
        str(author_api_info.author_unique_id)
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
    except Exception as ex:
        print('Failed to fetch data. Error:', ex)
        return

    author_api_info.status = 'IN_PROGRESS'
    author_api_info.save()

    if response.status_code == 200:
        for record in data['data']:
            try:
                author = Author.objects.get_or_create(
                    unique_id=record['unique_id'],
                    unique_uuid=record['unique_uuid'],
                    origin_unique_id=record['origin_unique_id'],
                    username=record['username'],
                    profile_text=record['texts']['profile_text'],
                    info = AuthorInfo.objects.create(
                        name=record['info']['name'],
                        platform=record['info']['platform'],
                    ),
                    avatar_url=None if not record['avatar']['urls'] else record['avatar']['urls'][0]
                )[0]
                AuthorStats.objects.create(
                    author=author,
                    follower_id=record['stats']['digg_count']['followers']['id'],
                    follower_count=record['stats']['digg_count']['followers']['count'],
                )
            except Exception as ex:
                print('Failed to save author details. Error:', ex)

        author_api_info.status = 'SUCCESS'
        author_api_info.save()
    else:
        author_api_info.status = 'FAILED'
        author_api_info.save()
        print("Failed to fetch data. Status code:", response.status_code)
        print(response.json())
