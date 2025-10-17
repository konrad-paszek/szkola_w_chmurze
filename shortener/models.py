from django.db import models

class Url(models.Model):
    short_url = models.CharField(max_length=255)
    original_url = models.URLField()
    short_string = models.CharField(max_length=6, unique=True)
