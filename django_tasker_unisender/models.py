import os

import requests
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Unisender:
    def __init__(self):
        self.api_key = getattr(settings, 'UNISENDER_API_KEY', os.environ.get('UNISENDER_API_KEY'))
        self.params = {'format': 'json', 'api_key': self.api_key}
        self.url = "https://api.unisender.com/ru/api"

    def create_list(self, title: str = None) -> int:
        params = self.params
        params['title'] = title

        response = requests.get(
            url="{url}/createList".format(url=self.url),
            params=params
        )

        if response.status_code == 200:
            json = response.json()
            return json.get("result").get("id")

    def delete_list(self, id: int) -> bool:
        params = self.params
        params['list_id'] = id
        response = requests.get(
            url="{url}/deleteList".format(url=self.url),
            params=params,
        )
        if response.status_code == 200:
            return True
        else:
            return False

    def update_list(self, id: int, title: str):
        params = self.params
        params['list_id'] = id
        params['title'] = title
        response = requests.get(
            url="{url}/updateList".format(url=self.url),
            params=params,
        )
        if response.status_code == 200:
            return True
        else:
            return False


class List(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"), unique=True)

    def __str__(self):
        return '{title}'.format(title=self.title)

    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")

    def delete(self, using=None, keep_parents=False):
        unisender = Unisender()
        unisender.delete_list(unisender_id=self.pk)
        super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        unisender = Unisender()

        if not self.pk or force_insert:
            self.pk = unisender.create_list(self.title)
        else:
            unisender.update_list(title=self.title, id=self.pk)

        super().save(force_insert, force_update, using, update_fields)
