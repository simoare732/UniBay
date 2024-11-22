from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    # Return the value of the dictionary with the key
    return dictionary.get(key)



@register.filter
def exclude_page(querydict):
    # Remove parameter 'page' from query
    qd = querydict.copy()
    qd.pop('page', None)  # Remove 'page' parameter if exists
    return qd.urlencode()

