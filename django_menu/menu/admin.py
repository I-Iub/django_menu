from django.contrib import admin

from .forms import MenuAdminForm
from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    form = MenuAdminForm
    list_display = (
        'pk', 'title', 'title_slug', 'path', 'name', 'level', 'url'
    )
    search_fields = ('title', 'title_slug', 'name', 'path')
    list_filter = ('title', 'title_slug')
    ordering = ['title_slug', 'path']
    empty_value_display = '-пусто-'

    def save_model(self, request, obj, form, change):
        obj.level = len(obj.path.split('-'))
        super(MenuAdmin, self).save_model(request, obj, form, change)


admin.site.register(Menu, MenuAdmin)
