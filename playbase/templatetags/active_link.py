from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, view_name, active_class='active', inactive_class=''):
    try:
        path = reverse(view_name)
    except NoReverseMatch:
        return inactive_class
    if context['request'].path == path:
        return active_class
    return inactive_class
