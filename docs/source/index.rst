Welcome to Django Tasker Unisender's documentation!
===================================================

.. image:: https://travis-ci.org/kostya-ten/django_tasker_unisender.svg?branch=master
    :target: https://travis-ci.org/kostya-ten/django_tasker_unisender

.. image:: https://readthedocs.org/projects/django-tasker-unisender/badge/?version=latest
    :target: https://django-tasker-unisender.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://api.codacy.com/project/badge/Grade/9fe057e68937477aab1aebd907aa0913
    :target: https://www.codacy.com/app/kostya/django_tasker_unisender?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kostya-ten/django_tasker_unisender&amp;utm_campaign=Badge_Grade

Requirements
""""""""""""""""""
* Python 3.6+
* A supported version of Django >= 2.0


Getting It
""""""""""""""""""

You can get Django Tasker Account by using pip::

    $ pip install django-tasker-unisender

If you want to install it from source, grab the git repository from GitHub and run setup.py::

    $ git clone git://github.com/kostya-ten/django_tasker_unisender.git
    $ cd django_tasker_unisender
    $ python setup.py install


Installation
""""""""""""""""""
To enable ``django_tasker_unisender`` in your project you need to add it to `INSTALLED_APPS` in your projects ``settings.py``

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'django_tasker_unisender',
        # ...
    )


.. toctree::
   :maxdepth: 2
   :caption: Modules:

   unisender


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
