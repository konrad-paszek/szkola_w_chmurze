from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import redirect

from .serializers import UrlSerializer
from .models import Url

class CreateUrlShortener(generics.CreateAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer

class RedirectToOriginalUrl(APIView):
    def get(self, _, short_string: str):
        url = get_object_or_404(Url, short_string=short_string)
        return redirect(url.original_url)