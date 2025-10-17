import pytest
from django.test import Client
from django.urls import reverse
from shortener.models import Url

pytestmark = pytest.mark.django_db

@pytest.fixture()
def url() -> Url:
    return Url.objects.create(original_url="https://github.com", short_url='http://testserver/f36UKX', short_string='f36UKX')

def test_create_short_url_valid(client: Client):
    response = client.post(reverse("shortener"), data={"original_url": "https://github.com"})
    assert response.status_code == 201
    assert response.json().get('short_url') is not None

def test_create_short_url_invalid_url(client: Client):
    response = client.post(reverse("shortener"), data={"original_url": "github.com"})
    assert response.status_code == 400
    assert response.content == (b'{"original_url":["Enter a valid URL."]}')

def test_create_short_url_already_existed_valid_response(client: Client, url: Url):
    response = client.post(reverse("shortener"), data={"original_url": "https://github.com"})
    assert response.status_code == 201
    assert response.json().get('short_url') == url.short_url


def test_redirect_by_short_url_valid(client: Client, url: Url):
    response = client.get(reverse("redirection", kwargs={"short_string": url.short_string}))
    assert response.status_code == 302
    assert response['Location'] == url.original_url