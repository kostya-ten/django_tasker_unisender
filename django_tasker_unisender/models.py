import os

import requests
from django.conf import settings
from django.core import validators
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from . import unisender


def _get_request(method: str = None, data: dict = None) -> object:
    url = "{url}/{method}".format(url="https://api.unisender.com/ru/api", method=method)
    api_key = getattr(settings, 'UNISENDER_API_KEY', os.environ.get('UNISENDER_API_KEY'))
    data = {**data, **{'format': 'json', 'api_key': api_key}}
    response = requests.request(method='POST', url=url, data=data)

    json = response.json()
    if json.get('error'):
        raise requests.HTTPError("Unisender error: {error}".format(error=json.get('error')))
    return json.get('result')


class List(models.Model):
    """
        Contact list model
    """
    title = models.CharField(max_length=200, verbose_name=_("Title"), unique=True)
    is_default = models.BooleanField(verbose_name=_("Default list"))

    def __str__(self):
        return '{title}'.format(title=self.title)

    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")

    def delete(self, using=None, keep_parents=False):
        unisender.delete_list(list_id=self.pk)
        super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk or force_insert:
            self.pk = unisender.create_list(title=self.title)
        else:
            unisender.update_list(list_id=self.pk, title=self.title)

        super().save(force_insert, force_update, using, update_fields)


class Field(models.Model):
    """
        Custom field model
    """
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
            self.pk = unisender.create_field(name=self.name, type=self.get_type_display(), public_name=self.public_name)
        else:
            unisender.update_field(id=self.pk, name=self.name, public_name=self.public_name)
            delattr(self, 'type')

        super().save(force_insert, force_update, using, update_fields)


class Subscribe(models.Model):
    email = models.EmailField(
        max_length=200,
        verbose_name=_("Email address"),
    )

    list = models.ForeignKey(List, on_delete=models.CASCADE)

    #list = models.ManyToManyField(List)
    #list_ids=17439493&double_optin=3&overwrite=1&fields[email]=test@example.org&fields[Names]=UserName

    def __str__(self):
        return '{email}'.format(email=self.email)

    class Meta:
        verbose_name = _("Subscribe")
        verbose_name_plural = _("Subscribes")
        unique_together = ("email", "list")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk or force_insert:
            self.pk = unisender.subscribe(list_ids=self.list.id, fields={'fields[email]': self.email})
            super().save(force_insert, force_update, using, update_fields)
        else:
            self.pk = unisender.subscribe(list_ids=self.list.id, fields={'fields[email]': self.email})
            super().save(force_insert, force_update, using, update_fields)

        super().save(force_insert, force_update, using, update_fields)

        # export = _get_request(
        #     method='exportContacts',
        #     data={
        #         'email': self.email,
        #     }
        # )
        #
        # for field in export.get('field_names'):
        #     print(field)
        #     #export.get('data')
        #
        #
        # person = _get_request(
        #     method='subscribe',
        #     data={
        #         'list_ids': self.list.pk,
        #         'fields[email]': self.email,
        #         'double_optin': 3,
        #         'overwrite': 1,
        #     }
        # )
        # self.pk = person.get('person_id')


    #def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        #if not self.pk or force_insert:

            # result_list = _get_request(method='createList', data={'title': 'tmp'})
            # list_id = result_list.get("result").get("id")
            #
            # person = _get_request(
            #     method='subscribe',
            #     data={
            #         'list_ids': list_id,
            #         'double_optin': 3,
            #         'overwrite': 1,
            #         'fields[email]': self.email,
            #     }
            # )
            #
            # self.pk = person.get('result').get('person_id')
            #
            # # Delete list
            # _get_request(method='deleteList', data={'list_id': list_id})

            #super().save(force_insert, force_update, using, update_fields)


        # for list in self.list.all():
        #     # result = _get_request(
        #     #   method='subscribe',
        #     #   data={
        #     #       'list_ids': list.id,
        #     #       'double_optin': 3,
        #     #       'overwrite': 1,
        #     #       'fields[email]': self.email,
        #     #   }
        #     # )
        #     # #result.get('')
        #     print(list)



        #ff = self.list
        #print(ff.all())

        #self.email = "kostya@bk.ru"
        #self.pk = 3

        #super().save(force_insert, force_update, using, update_fields)



        #if not self.pk or force_insert:
        #    print(self.list)

            #self.list
            #print(self.list.obj)

            #for tag in self.list:
            #    print(tag.id)



            #self.
            #print(self.list.)

            #for list in :
            #    print(list)

            #list_default = List.objects.filter(is_default=1)
            #if list_default.count():
            #    print('sss')
                # print(list_default.last().)

            #print(self.list.all())
            #result = _get_request(
            #   method='subscribe',
            #   data={
            #       'list_ids': self.list,
            #       'double_optin': 3,
            #       'overwrite': 1,
            #       'fields[email]': self.email,
            #   }
            #)
            #self.pk = result.get('result').get('id')

        # else:
        #     _get_request(
        #        method='updateField',
        #        data={
        #            'id': self.pk,
        #            'name': self.name,
        #            'public_name': self.public_name,
        #        }
        #     )
        #     delattr(self, 'type')


# Signals
# @receiver(pre_save, sender=List)
# def modelList(instance=None, **kwargs):
#     pass

    #if not instance.pk:
    #    result = _get_request(method='createList', data={'title': instance.title})
    #    instance.pk = result.get("result").get("id")
    #    instance.save()
    #else:
    #    print('update')

    #print(instance.title)
    #print(instance.pk)
    #print(instance.is_default)

    #raise requests.HTTPError("Test error")

