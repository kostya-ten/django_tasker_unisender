import os

import requests
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Unisender:
    def __init__(self):
        self.api_key = getattr(settings, 'UNISENDER_API_KEY', os.environ.get('UNISENDER_API_KEY'))
        self.params = {'format': 'json', 'api_key': self.api_key}
        self.url = "https://api.unisender.com/ru/api/"

    def create_list(self, title: str = None) -> int:
        params = self.params
        params['title'] = title

        response = requests.get(
            url="{url}/createList".format(url=self.url),
            params=params
        )
        if response.status_code == 200:
            return response.json().get("result").get("id")


class List(models.Model):
    unisender_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name=_("Title"))

    def __str__(self):
        return '{title}'.format(title=self.title)

    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")

    def delete(self, using=None, keep_parents=False):
        print('delete')

    def save(self, *args, **kwargs):
        if not self.pk or kwargs.get('force_insert', False):
            unisender = Unisender()
            self.unisender_id = unisender.create_list(self.title)

        super().save(*args, **kwargs)


