# Generated by Django 2.2 on 2019-04-17 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_tasker_unisender', '0003_auto_20190417_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('type', models.SmallIntegerField(choices=[(1, 'string'), (2, 'text'), (3, 'number'), (4, 'date'), (5, 'bool')], verbose_name='Name')),
                ('public_name', models.SmallIntegerField(max_length=200, verbose_name='Public name')),
            ],
            options={
                'verbose_name': 'Field',
                'verbose_name_plural': 'Fields',
            },
        ),
    ]
