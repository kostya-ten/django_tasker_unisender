from django.db import models
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
            list_ids=self.UnisenderMeta.list_id,
            fields=fields,
        )
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        unisender = Unisender()
        unisender.exclude(contact_type="email", contact=self.email, list_ids=[self.UnisenderMeta.list_id])
        super().delete(using, keep_parents)



# Signals
# @receiver(pre_save, sender=User)
# def modelList(instance=None, **kwargs):
#     pass
