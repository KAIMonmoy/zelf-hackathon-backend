from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status

from .documents import ContentDocument, AuthorDocument

@api_view(['GET'])
def get_content_list(request):
    # Get page number from request query
    page = request.GET.get('page')

    # Search for contents with page_number=page
    content_query = ContentDocument.search().query("match", page_number=page)
    contents = content_query.execute()

    # Get unique author ids from contents
    author_ids = [content.author_unique_id for content in contents]

    # Search for authors with unique ids
    author_query = AuthorDocument.search().query("terms", unique_id=author_ids)
    authors = author_query.execute()

    # Create a dictionary of authors with unique ids as keys
    author_dict = {str(author.unique_id): author for author in authors}

    content_list = []
    # Update contents with respective authors
    for content in contents:
        content_dict = content.to_dict()
        author = author_dict.get(str(content.author_unique_id))
        content_dict['author'] = {} if not author else author.to_dict()
        content_list.append(content_dict)
        print(content_dict)
    


    # Return contents with respective authors
    return JsonResponse({
            'data': content_list
        }, 
        status=status.HTTP_200_OK
    )
