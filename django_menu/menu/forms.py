import os

from django import forms
from django.core.exceptions import ValidationError
from dotenv import load_dotenv

from .models import Menu

load_dotenv()


class MenuAdminForm(forms.ModelForm):
    class Meta:
        exclude = ['level']
        model = Menu

    def clean_path(self):
        cleaned_data = super().clean()
        slug = cleaned_data['title_slug']
        form_path = cleaned_data['path']
        parent_path = '-'.join(form_path.split('-')[:-1])
        parent_item = Menu.objects.filter(path=parent_path,
                                          title_slug=slug).exists()
        if parent_path and not parent_item:
            raise ValidationError('Для указанного пути нет родителя')

        duplicate = Menu.objects.filter(path=form_path,
                                        title_slug=slug).exists()
        if duplicate:
            raise ValidationError('Такой путь уже занят')

        parent_item = Menu.objects.get(title_slug=slug, path=parent_path)
        valid_parent_url = (
            f'{os.getenv("HOST_URL")}/menu/{slug}/{parent_item.url}'
        )
        if parent_item.url != valid_parent_url:
            raise ValidationError(
                'Родительский пункт содержит недопустимый url'
            )
        return form_path

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data['title']
        slug = cleaned_data['title_slug']
        item = Menu.objects.filter(title_slug=slug).first()
        if item and item.title != title:
            raise ValidationError(
                'Название %(form_title)s должно совпадать с имеющимся в БД'
                '"%(db_title)s" для указанного слага',
                params={'form_title': title,
                        'db_title': item.title}
            )
        return cleaned_data
