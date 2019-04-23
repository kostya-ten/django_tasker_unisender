Welcome to Django Tasker Unisender's documentation!
===================================================

.. image:: https://travis-ci.org/kostya-ten/django_tasker_unisender.svg?branch=master
    :target: https://travis-ci.org/kostya-ten/django_tasker_unisender

.. image:: https://readthedocs.org/projects/django-tasker-unisender/badge/?version=latest
    :target: https://django-tasker-unisender.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://api.codacy.com/project/badge/Grade/9fe057e68937477aab1aebd907aa0913
    :target: https://www.codacy.com/app/kostya/django_tasker_unisender?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kostya-ten/django_tasker_unisender&amp;utm_campaign=Badge_Grade

.. image:: https://requires.io/github/kostya-ten/django_tasker_unisender/requirements.svg?branch=master
     :target: https://requires.io/github/kostya-ten/django_tasker_unisender/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://badge.fury.io/py/django-tasker-unisender.svg
    :target: https://badge.fury.io/py/django-tasker-unisender


Requirements
""""""""""""""""""
* Python 3.6+
* A supported version of Django >= 2.0


Installation
""""""""""""""""""

You can get Django Tasker Unisender by using pip::

    $ pip install django-tasker-unisender


To enable ``django_tasker_unisender`` in your project you need to add it to `INSTALLED_APPS` in your projects ``settings.py``

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'django_tasker_unisender',
        # ...
    )

Add to your ``settings.py``

.. code-block:: python

    UNISENDER_API_KEY="<< YOU API KEY>>"

You can get the api key at this `link <https://www.unisender.com/?a=ndix/>`_

Add to your ``models.py``

.. code-block:: python

    from django_tasker_unisender.models import EmailModel

    class Subscribe(EmailModel):

        class UnisenderMeta:
            list_id = 123456789 # Your list id contact on Unisender



Migrate your project

.. code-block:: shell

    python manage.py makemigrations
    python manage.py migrate

Add to your ``admin.py``

.. code-block:: python

    from django.contrib import admin
    from . import models

    class SubscribeAdmin(admin.ModelAdmin):
        list_display = ('email',)

    admin.site.register(models.Subscribe, SubscribeAdmin)

`Full documentation <https://django-tasker-unisender.readthedocs.io/>`_