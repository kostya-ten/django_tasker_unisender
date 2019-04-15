from setuptools import setup

setup(
    name='django_unisender',
    version='0.1',
    packages=['tests', 'unisender', 'unisender.migrations'],
    url='https://github.com/kostya-ten/django_unisender',
    license='Apache License 2.0',
    author='kostya',
    author_email='kostya@yandex.ru',
    description='UniSender - service for mass email'
)
