from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin

from .models import Node, Menu


class MenuInline(StackedInline):
    model = Menu
    extra = 0


class TreeThingInline(StackedInline):
    model = Node
    extra = 0


@admin.register(Node)
class TreeThingAdmin(ModelAdmin):
    list_display = ("id", "name", "parent", "menu")
    inlines = [TreeThingInline]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Menu)
class MenuAdmin(ModelAdmin):
    list_display = ("id", "name",)
