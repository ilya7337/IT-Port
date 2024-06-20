from django import template

register = template.Library()

@register.filter(name="addclass")
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name="add_placeholder")
def add_attributes(field, value):
    attrs = dict(field.field.widget.attrs)
    attrs["placeholder"] = value
    return field.as_widget(attrs=attrs)
