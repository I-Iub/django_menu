import os

from django import template
from django.http import Http404
from django.template.context import RequestContext
from dotenv import load_dotenv

from ..models import Menu
from .utils import MenuPath, extend_by_parents, get_item_path

load_dotenv()
register = template.Library()
IDENT = 40
MENU_URL = f'{os.getenv("HOST_URL")}menu/'


@register.simple_tag(takes_context=True)
def draw_menu(context: RequestContext, draw_title: str) -> str:
    request = context.get('request')
    item_path = get_item_path(request.path)
    if (item_path is not None and
            item_path.title_slug == draw_title and
            item_path.path is not None):
        return get_expanded_menu(draw_title, item_path)
    else:
        return get_collapsed_menu(draw_title, item_path)


def get_collapsed_menu(draw_title: str, item_path: MenuPath | None) -> str:
    top_items = Menu.objects.filter(
        title_slug=draw_title, level=1
    ).order_by('path')
    if not top_items:
        return ''
    header_title = top_items[0].title
    header = get_header(draw_title, item_path, header_title)
    return get_menu_html(header, top_items)


def get_expanded_menu(draw_title: str, item_path: MenuPath) -> str:
    top_items = Menu.objects.filter(title_slug=draw_title, level=1)
    paths = extend_by_parents(item_path)
    item_level = len(paths)
    all_items = top_items.union(
        Menu.objects.filter(title_slug=draw_title, path__in=paths),
        Menu.objects.filter(title_slug=draw_title,
                            path__startswith=item_path.path,
                            level=item_level + 1)
    ).order_by('path')

    wrong_path = True
    for db_item in all_items:
        if db_item.path == item_path.path:
            wrong_path = False
            break
    if wrong_path:
        raise Http404

    header_title = all_items[0].title
    header = get_header(draw_title, item_path, header_title)
    return get_menu_html(header, all_items)


def get_header(
        draw_title: str, item_path: MenuPath | None, menu_title: str
) -> str:
    menu_url = f'{MENU_URL}{draw_title}/'
    header_template = f'<h3><a href="{menu_url}"%s> {menu_title} </a></h3>'
    if item_path is not None and item_path.title_slug == draw_title:
        header = header_template % ' style="color:rgb(255,0,0)"'
    else:
        header = header_template % ''
    return header


def get_menu_html(header: str, items: list[Menu]) -> str:
    html = [header] + ['<ul>']
    menu_html = [
        (f'<li style="text-indent: {IDENT * item.level}px">'
         f'<a href="{item.url}">{item.name}</a></li>') for item in items
    ]
    html += menu_html + ['</ul>']
    return ''.join(html)
