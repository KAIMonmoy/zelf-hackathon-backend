from django.http import HttpResponse
from contents.tasks import fetch_contents, fetch_author_details

def test_content(request):
    fetch_contents.delay()
    return HttpResponse("ok")


def test_author(request):
    fetch_author_details.delay()
    return HttpResponse("ok")
