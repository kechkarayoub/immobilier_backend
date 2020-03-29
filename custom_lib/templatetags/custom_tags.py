from django import template

register = template.Library()


def get_value(dictionary, key):
    return dictionary.get(key)


register.filter('get_value', get_value)
