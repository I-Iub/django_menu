from dataclasses import dataclass


@dataclass
class MenuPath:
    title_slug: str
    path: str = None


def get_item_path(path: str) -> MenuPath | None:
    path = path.strip('/').split('/')[1:]
    if not path:
        return
    url_path = MenuPath(title_slug=path[0])
    if len(path) > 1:
        url_path.path = path[1]
    return url_path


def extend_by_parents(path: MenuPath) -> list[str]:
    parts = path.path.split('-')
    parent_paths = []
    current_path = ''
    for part in parts:
        if not current_path:
            current_path = part
        else:
            current_path += '-' + part
        parent_paths.append(current_path)
    return parent_paths
