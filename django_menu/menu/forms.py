import os
import typing

from django import forms
from django.core.exceptions import ValidationError
from dotenv import load_dotenv

from .models import Menu

load_dotenv()
item_url_template = f'{os.getenv("HOST_URL")}menu/%s/%s'


class MenuAdminForm(forms.ModelForm):
    url = forms.URLField(label='URL', required=False)

    class Meta:
        exclude = ['level']
        model = Menu

    def clean(self):
        cleaned_data = super().clean()
        title = get_field(cleaned_data, 'title')
        slug = get_field(cleaned_data, 'title_slug')

        item = Menu.objects.filter(title_slug=slug).first()
        if item and item.title != title:
            raise ValidationError(
                'Название %(form_title)s должно совпадать с имеющимся в БД '
                'названием "%(db_title)s" для указанного слага',
                params={'form_title': title,
                        'db_title': item.title}
            )

        form_path = get_field(cleaned_data, 'path')
        parent_path = '-'.join(form_path.split('-')[:-1])
        check_path(slug, parent_path)
        url = get_field(cleaned_data, 'url')
        if not url:
            cleaned_data['url'] = item_url_template % (slug, form_path)

        return cleaned_data


def get_field(data: dict, field: str) -> typing.Any:
    if (value := data.get(field)) is None:
        raise ValidationError(f'Заполните поле "{field}"')
    return value


def check_path(slug: str, parent_path: str) -> None:
    parent_item = Menu.objects.filter(path=parent_path,
                                      title_slug=slug).first()
    if parent_path and parent_item is None:
        raise ValidationError('Для указанного пути нет родителя')

    if parent_item is not None:
        valid_parent_url = item_url_template % (slug, parent_path)
        if parent_item.url != valid_parent_url:
            raise ValidationError(
                'Родительский пункт содержит недопустимый url'
            )
