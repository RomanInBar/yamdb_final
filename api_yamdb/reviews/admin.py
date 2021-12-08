from django.contrib import admin
from django.db.models import Avg
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from reviews import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'username', 'role')
    search_fields = ('username__startswith',)
    list_filter = ('role',)


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'year', 'rating')
    list_filter = ('category',)
    search_fields = ('name__startswith',)

    def rating(self, obj):
        result = obj.reviews.aggregate(Avg('score'))
        return result['score__avg']


def link(count, url):
    if (count % 10) in range(2, 5) and count not in [12, 13, 14]:
        title = 'произведения'
    elif (count % 10) == 1 and count != 11:
        title = 'произведение'
    else:
        title = 'произведений'
    return format_html('<a href="{}">{} {}</a>', url, count, title)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'title_link')
    list_filter = ('name',)

    def title_link(self, obj):
        count = obj.titles.count()
        url = (
            reverse('admin:reviews_title_changelist')
            + '?'
            + urlencode({'category__id': f'{obj.id}'})
        )
        return link(count, url)

    title_link.short_description = 'titles'


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'title_link')
    list_filter = ('name',)

    def title_link(self, obj):
        count = obj.titles.count()
        url = (
            reverse('admin:reviews_title_changelist')
            + '?'
            + urlencode({'genre__id': f'{obj.id}'})
        )
        return link(count, url)

    title_link.short_description = 'titles'


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'pub_date', 'review')
    search_fields = ('pub_date', 'author__username__startswith')


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'text', 'score', 'pub_date')
    search_fields = ('author__username__startswith', 'pub_date')
    list_filter = ('title',)
