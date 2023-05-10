from django.contrib import admin
from reviews.models import Categories, Genres, Titles

from .models import User, Review, Comment

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)


class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'


@admin.register(Categories)
class CategoryAdmin(BaseAdmin):
    pass


@admin.register(Genres)
class GenreAdmin(BaseAdmin):
    pass


@admin.register(Titles)
class TitleAdmin(BaseAdmin):
    pass

