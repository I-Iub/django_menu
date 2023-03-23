from django import forms
from django.contrib import admin

from .models import Menu


class MenuAdminForm(forms.ModelForm):
    class Meta:
        exclude = ['level']
        model = Menu


class MenuAdmin(admin.ModelAdmin):
    form = MenuAdminForm
    list_display = (
        'pk', 'title', 'title_slug', 'path', 'name', 'level', 'url'
    )
    search_fields = ('title', 'title_slug', 'name', 'path')
    list_filter = ('title', 'title_slug')
    empty_value_display = '-пусто-'

    # def save_model(self, request, obj, form, change):
    #     obj.parent = get_parent(obj.path)
    #     super(MenuAdmin, self).save_model(request, obj, form, change)


admin.site.register(Menu, MenuAdmin)
