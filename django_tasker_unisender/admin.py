from django.contrib import admin
from . import models


class ListAdmin(admin.ModelAdmin):
    list_display = ('title',)
    readonly_fields = ('unisender_id',)


admin.site.register(models.List, ListAdmin)
