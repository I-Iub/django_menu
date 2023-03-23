from django.contrib import admin

from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'path', 'name', 'level', 'url')
    search_fields = ('title', 'name', 'path')
    list_filter = ('title',)
    empty_value_display = '-пусто-'

    # def save_model(self, request, obj, form, change):
    #     obj.parent = get_parent(obj.path)
    #     super(MenuAdmin, self).save_model(request, obj, form, change)


admin.site.register(Menu, MenuAdmin)
