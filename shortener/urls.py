from django.urls import path
from . import views

urlpatterns = [
    path("url-shortener/", views.CreateUrlShortener.as_view(), name='shortener'),
    path("<short_string>/", views.RedirectToOriginalUrl.as_view(), name='redirection')
]