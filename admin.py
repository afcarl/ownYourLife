from django.contrib import admin

from ownYourLife.models import Category, Entry, Tag

admin.site.register(Entry)
admin.site.register(Category)
admin.site.register(Tag)
