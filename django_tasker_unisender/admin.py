from django.contrib import admin
from . import models


class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_default')
    #readonly_fields = ('unisender_id',)


class FieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'public_name')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')


admin.site.register(models.List, ListAdmin)
admin.site.register(models.Field, FieldAdmin)
admin.site.register(models.Subscribe, SubscribeAdmin)
