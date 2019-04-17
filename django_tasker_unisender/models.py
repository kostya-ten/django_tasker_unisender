import os

import requests
from django.conf import settings
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


def _get_request(method: str = None, data: dict = None) -> object:
    url = "{url}/{method}".format(url="https://api.unisender.com/ru/api", method=method)
    api_key = getattr(settings, 'UNISENDER_API_KEY', os.environ.get('UNISENDER_API_KEY'))
    data = {**data, **{'format': 'json', 'api_key': api_key}}
    response = requests.request(method='POST', url=url, data=data)

    json = response.json()
    if json.get('error'):
        raise requests.HTTPError(json.get('error'))
    return json


class List(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Title"), unique=True)
    is_default = models.NullBooleanField(verbose_name=_("Default list"), null=True, unique=True)

    def __str__(self):
        return '{title}'.format(title=self.title)

    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")

    def delete(self, using=None, keep_parents=False):
        _get_request(method='deleteList', data={'list_id': self.pk})
        super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk or force_insert:
            result = _get_request(method='createList', data={'title': self.title})
            self.pk = result.get("result").get("id")
        else:
            _get_request(method='updateList', data={'list_id': self.pk})

        super().save(force_insert, force_update, using, update_fields)


class Field(models.Model):
    TYPE = (
        (1, 'string'),
        (2, 'text'),
        (3, 'number'),
        (4, 'date'),
        (5, 'bool'),
    )

    name = models.CharField(
        max_length=78,
        verbose_name=_("Name"),
        validators=[
            validators.RegexValidator(
                regex=r'^[0-9a-zA-Z]+$',
                message=_('Use the format 0-9 a-z.')
            )
        ],
        help_text=_("Variable to be substituted. It must be unique and case sensitive. "
                    "Also, it is not recommended to create a field with the same name as the standard field names "
                    "(tags, email, phone, email_status, phone_status, etc.)"),
        unique=True
    )

    type = models.SmallIntegerField(
        choices=TYPE,
        verbose_name=_("Type"),
        null=True,
        help_text=_("The field type is relevant only for the web interface, "
                    "the controls are adjusted to the possible values. "
                    "Values of different types are stored in the same way, in the text form.")
    )

    public_name = models.CharField(
        max_length=200,
        verbose_name=_("Public name"),
        help_text=_("Field name. If it is not used, an automatical generation by the «name» field will take place.")
    )

    def __str__(self):
        return '{title} {public_name}'.format(title=self.name, public_name=self.public_name)

    class Meta:
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")

    def delete(self, using=None, keep_parents=False):
        _get_request(method='deleteField', data={'id': self.pk})
        super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk or force_insert:
            result = _get_request(
               method='createField',
               data={
                   'name': self.name,
                   'type': self.get_type_display(),
                   'public_name': self.public_name,
               }
            )
            self.pk = result.get('result').get('id')
        else:
            _get_request(
               method='updateField',
               data={
                   'id': self.pk,
                   'name': self.name,
                   'public_name': self.public_name,
               }
            )
            delattr(self, 'type')

        super().save(force_insert, force_update, using, update_fields)

# class Subscribe(models.Model):
#     email = models.EmailField(
#         max_length=200,
#         verbose_name=_("Email address")
#     )
#
#     list = models.ManyToManyField(List)
#
#     pass
