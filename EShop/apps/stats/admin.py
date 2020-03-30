from django.contrib import admin
from apps.stats.models import Stat


class StatAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)


# Register your models here.
admin.site.register(Stat, StatAdmin)
