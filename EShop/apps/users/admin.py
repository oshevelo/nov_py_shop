from django.contrib import admin
from apps.users.models import UserProfile, UserAddress, UserPhone

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserAddress)
admin.site.register(UserPhone)
