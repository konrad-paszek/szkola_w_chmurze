import pytest
from unittest.mock import patch
from django.db import IntegrityError
from rest_framework.test import APIRequestFactory
from shortener.serializers import UrlSerializer
from shortener.models import Url
from rest_framework import serializers

pytestmark = pytest.mark.django_db

payload = {'original_url': 'https://github.com'}

@pytest.fixture()
def url() -> Url:
    return Url.objects.create(original_url="https://github.com", short_url='http://testserver/f36UKX', short_string='f36UKX')


def test_url_serializer_valid():
    factory = APIRequestFactory()
    request = factory.post('/')
    serializer = UrlSerializer(data=payload, context={'request': request})
    assert serializer.is_valid()
    instance = serializer.save()
    assert instance.original_url == payload['original_url']
    assert instance.short_string is not None
    assert instance.short_url is not None


def test_url_serializer_duplicate(url: Url):
    factory = APIRequestFactory()
    request = factory.post('/')
    serializer = UrlSerializer(data=payload, context={'request': request})
    assert serializer.is_valid()
    instance = serializer.save()
    assert instance.original_url == payload['original_url']
    assert instance.short_string == url.short_string


def test_url_serializer_invalid():
    invalid_payload = {'original_url': 'invalid-url'}
    serializer = UrlSerializer(data=invalid_payload)
    assert not serializer.is_valid()
    assert 'original_url' in serializer.errors


def always_integrity_error(*args, **kwargs):
    raise IntegrityError

@patch('shortener.serializers.Url.objects.create', side_effect=always_integrity_error)
@patch('shortener.serializers.Url.objects.exists', return_value=False)
def test_create_raises_validation_error(mock_filter, mock_create):
    serializer = UrlSerializer(data=payload)
    serializer.is_valid()
    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.save()
    assert "Failed to create a unique short URL" in str(exc_info.value)