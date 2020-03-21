from django.contrib import admin
from .models import Notificator


class NotificAdmin(admin.ModelAdmin):
    list_display = ('notification_who', 'notification_what', 'notification_date', 'notification_how')


admin.site.register(Notificator, NotificAdmin)