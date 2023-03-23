import os

from django import template
from django.http import Http404
from django.template.context import RequestContext
from dotenv import load_dotenv

from .utils import MenuPath, extend_by_parents, get_item_path
from ..models import Menu

load_dotenv()
register = template.Library()
IDENT = 40
MENU_URL = f'{os.getenv("HOST_URL")}menu/'


@register.simple_tag(takes_context=True)
def draw_menu(context: RequestContext, draw_title: str) -> str:
    request = context.get('request')
    item_path = get_item_path(request.path)

    menu_url = f'{MENU_URL}{draw_title}/'
    header_template = f'<h3><a href="{menu_url}"%s> {draw_title} </a></h3>'
    if item_path is not None and item_path.title == draw_title:
        header = header_template % ' style="color:rgb(255,0,0)"'
    else:
        header = header_template % ''

    if (item_path is not None and
            item_path.title == draw_title and
            item_path.path is not None):
        menu_html = get_expanded_menu(draw_title, item_path)
    else:
        menu_html = get_collapsed_menu(draw_title)
    if not menu_html:
        return header + '<p>-пусто-</p>'

    html = header + '<ul>'
    html += menu_html + '</ul>'
    return html


def get_collapsed_menu(draw_title: str) -> str:
    top_items = Menu.objects.filter(title=draw_title, level=1).order_by('path')
    html = [
        (f'<li style="text-indent: {IDENT}px">'
         f'<a href="{item.url}">{item.name}</a><br>') for item in top_items
    ]
    return ''.join(html)


def get_expanded_menu(title: str, item_path: MenuPath) -> str:
    top_items = Menu.objects.filter(title=title, level=1)
    paths = extend_by_parents(item_path)
    item_level = len(paths)
    all_items = top_items.union(
        Menu.objects.filter(title=title, path__in=paths),
        Menu.objects.filter(
            title=title, path__startswith=item_path.path, level=item_level + 1
        )
    ).order_by('path')

    wrong_path = True
    for db_item in all_items:
        if db_item.path == item_path.path:
            wrong_path = False
            break
    if wrong_path:
        raise Http404

    html = [
        (f'<li style="text-indent: {IDENT * item.level}px">'
         f'<a href="{item.url}">{item.name}</a></li>') for item in all_items
    ]
    return ''.join(html)
