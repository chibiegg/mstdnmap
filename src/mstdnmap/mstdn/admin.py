from django.contrib import admin

from mstdnmap.mstdn.models import Instance


class InstanceAdmin(admin.ModelAdmin):
    list_fields = ["id", "hostname"]


admin.site.register(Instance, InstanceAdmin)
