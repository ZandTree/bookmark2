from django import template


register = template.Library()

@register.inclusion_tag('_tags/collections_modal.html',takes_context=True)
def collection_modal(context):
    user  = context.get('user')
    return {'collections': user.collections.all()}
