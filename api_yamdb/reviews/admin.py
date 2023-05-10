from django.contrib import admin

from .models import User

admin.site.register(User)


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
