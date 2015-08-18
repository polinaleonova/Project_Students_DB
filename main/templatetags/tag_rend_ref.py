from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def rend_reference(context, entity):
    print entity
    if 'id_student' in entity.keys():
        url = '<a href="/admin/models_project/student/{}/">' \
              'Edit in Admin Panel</a>'.format(entity.get('id_student'))
    else:
        url = '<a href="/admin/models_project/group/{}/">' \
              'Edit in Admin Panel</a>'.format(entity.get('id_group'))
    return url
