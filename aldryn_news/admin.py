# -*- coding: utf-8 -*-
from django.contrib import admin

from aldryn_news.forms import NewsForm, CategoryForm
from aldryn_news.models import News, Category, Tag, TaggedItem

import cms
from cms.admin.placeholderadmin import PlaceholderAdmin
from cms.admin.placeholderadmin import FrontendEditableAdmin
from distutils.version import LooseVersion
from hvad.admin import TranslatableAdmin


class NewsAdmin(FrontendEditableAdmin, TranslatableAdmin, PlaceholderAdmin):

    list_display = ['__unicode__', 'publication_start', 'publication_end', 'all_translations']
    form = NewsForm
    frontend_editable_fields = ('title', 'lead_in', 'link')

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['title', 'slug', 'category', 'publication_start', 'publication_end']}),
            (None, {'fields': ['key_visual', 'lead_in', 'link', 'tags']})
        ]

        # show placeholder field if not CMS 3.0
        if LooseVersion(cms.__version__) < LooseVersion('3.0'):
            fieldsets.append(
                ('Content', {
                    'classes': ['plugin-holder', 'plugin-holder-nopage'],
                    'fields': ['content']}))

        return fieldsets

admin.site.register(News, NewsAdmin)


class CategoryAdmin(TranslatableAdmin):

    form = CategoryForm
    list_display = ['__unicode__', 'all_translations', 'ordering']
    list_editable = ['ordering']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['name', 'slug']}),
        ]
        return fieldsets

admin.site.register(Category, CategoryAdmin)


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


class TagAdmin(TranslatableAdmin):

    list_display = ['__unicode__', 'all_translations']
    inlines = [TaggedItemInline]

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['name', 'slug']}),
        ]
        return fieldsets


admin.site.register(Tag, TagAdmin)
