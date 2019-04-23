from django_tasker_unisender.models import EmailModel
from django.db import models


class Subscribe(EmailModel):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)

    class UnisenderMeta:
        list_id = 9147867
        fields = ['firstname', 'lastname']


class SubscribeTest(EmailModel):

    class UnisenderMeta:
        list_id = 17462165
