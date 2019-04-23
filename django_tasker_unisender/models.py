from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .unisender import Unisender


class EmailModel(models.Model):
    email = models.EmailField(max_length=255, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        unisender = Unisender()

        fields = {'fields[email]': self.email}

        if hasattr(self, 'UnisenderMeta') and hasattr(self.UnisenderMeta, 'fields'):
            for field in self.UnisenderMeta.fields:
                fields['fields[{field}]'.format(field=field)] = getattr(self, field)

        self.pk = unisender.subscribe(
            list_ids=[self.UnisenderMeta.list_id],
            fields=fields,
        )
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        unisender = Unisender()
        unisender.exclude(contact_type="email", contact=self.email, list_ids=[self.UnisenderMeta.list_id])
        super().delete(using, keep_parents)


@receiver(post_save, sender=User)
def unisenderuser_save(instance: User = None, **kwargs):
    if settings.UNISENDER_AUTO_LIST_ID and instance.email:
        fields = {
            'fields[email]': instance.email,
            'fields[last_name]': instance.last_name,
            'fields[first_name]': instance.first_name
        }

        unisender = Unisender()
        unisender.subscribe(
            list_ids=[settings.UNISENDER_AUTO_LIST_ID],
            fields=fields,
        )


@receiver(post_delete, sender=User)
def unisenderuser_delete(instance: User = None, **kwargs):
    if settings.UNISENDER_AUTO_LIST_ID and instance.email:
        unisender = Unisender()
        unisender.exclude(contact_type="email", contact=instance.email, list_ids=[settings.UNISENDER_AUTO_LIST_ID])
