from django.contrib import admin

from .models import User, Review, Comment, Category, Genre

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Genre)


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
