from django.db import IntegrityError
from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import Url

SHORT_STRING_LENGTH = 6

RETRY_ATTEMPTS = 20

class UrlSerializer(serializers.ModelSerializer):
    original_url = serializers.URLField(write_only=True)
    short_url = serializers.ReadOnlyField()

    class Meta:
        model = Url
        fields = [
            "original_url",
            "short_url"
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if not Url.objects.filter(original_url=validated_data['original_url']).exists():
            for _ in range(RETRY_ATTEMPTS):
                short_string = get_random_string(SHORT_STRING_LENGTH)
                validated_data['short_string'] = short_string
                if request:
                    validated_data['short_url'] = request.build_absolute_uri(f'/{short_string}')
                try:
                    return Url.objects.create(**validated_data)
                except IntegrityError:
                    continue
        else:
            return Url.objects.get(original_url=validated_data['original_url'])
        raise serializers.ValidationError(f"Failed to create a unique short URL after {RETRY_ATTEMPTS} attempts.")
