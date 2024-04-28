from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def use_icon(context, template_name):
    try:
        _template = get_template(f"partial/icon/{template_name}.html")
        return mark_safe(_template.render(context.flatten()))
    except template.TemplateDoesNotExist:
        return mark_safe("<!-- Template not found: {} -->".format(template_name))
