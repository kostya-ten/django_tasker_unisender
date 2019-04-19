from django.contrib import admin
from . import models


# class ListAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'is_default')
#     actions = None
#
#
# class FieldAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'type', 'public_name')
#     actions = None
#
#
# class SubscribeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'email')
#     actions = None
#
#
# admin.site.register(models.List, ListAdmin)
# admin.site.register(models.Field, FieldAdmin)
# admin.site.register(models.Subscribe, SubscribeAdmin)
admin.site.register(models.Subscribe)
admin.site.register(models.SubscribeTest)
