from django.db import models


class Books(models.Model):

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=255, null=True, blank=True)
    pages = models.SmallIntegerField(null=True, blank=True)
    cover = models.URLField(null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.author}"
