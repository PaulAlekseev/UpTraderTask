from django import template
from django.template import RequestContext

from tree.models import Node

register = template.Library()


@register.simple_tag(name="get_with_key")
def get_with_key(dictionary: dict, key):
    return dictionary.get(key)


@register.inclusion_tag("tree/tree_menu.html", takes_context=True)
def draw_menu(context: RequestContext, menu_name):
    name = context.request.path_info[1:]
    items = Node.objects \
        .filter(menu__name=menu_name) \
        .select_related("parent") \
        .select_related("parent__parent")
    result = list(items)
    if len(result) == 0:
        return {"menu_name": menu_name}
    chosen_item = get_with_slug(result, name)
    result_dict, flat_dict = form_data(result)
    return {"chosen_node": chosen_item, "result_dict": result_dict, "flat_dict": flat_dict, "menu_name": menu_name}


@register.inclusion_tag("tree/tree_branch.html", takes_context=True)
def draw_node(context, dictionary, chosen_node, flat_dict):
    return {"chosen_node": chosen_node, "result_dict": dictionary, "flat_dict": flat_dict}


def get_with_slug(items: list[Node], slug: str) -> Node:
    for item in items:
        if item.slug == slug:
            return item


def form_data(items: list[Node]):
    result_dict = {-1: ({}, None)}
    flat_dict = {}
    for item in items:
        flat_dict.update({item.id: item})
        if item.parent is None:
            result_dict[-1][0].update({item.id: item})
            continue
        if item.parent.id not in result_dict.keys():
            parent = item.parent
            parent_parent_id = parent.parent.id if parent.parent is not None else -1
            result_dict.update({parent.id: ({}, parent_parent_id)})
        result_dict[item.parent.id][0].update({item.id: item})
    return result_dict, flat_dict
