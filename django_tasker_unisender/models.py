import os

import requests
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class List(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"), unique=True)

    def __str__(self):
        return '{title}'.format(title=self.title)

    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")

    def delete(self, using=None, keep_parents=False):
        self._get_request(method='deleteList', data={'list_id': self.pk})
        super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk or force_insert:
            result = self._get_request(method='createList', data={'title': self.title})
            self.pk = result.get("result").get("id")
        else:
            self._get_request(method='updateList', data={'list_id': self.pk})

        super().save(force_insert, force_update, using, update_fields)

    @staticmethod
    def _get_request(method: str = None, data: dict = None) -> object:
        url = "{url}/{method}".format(url="https://api.unisender.com/ru/api", method=method)
        api_key = getattr(settings, 'UNISENDER_API_KEY', os.environ.get('UNISENDER_API_KEY'))
        data = {**data, **{'format': 'json', 'api_key': api_key}}
        response = requests.request(method='POST', url=url, data=data)

        json = response.json()
        if json.get('error'):
            raise requests.HTTPError(json.get('error'))
        return json