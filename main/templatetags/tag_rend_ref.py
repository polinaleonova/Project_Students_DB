from django import template
from models_project import models

register = template.Library()


# @register.inclusion_tag('refer_to_admin_edit.html')
@register.simple_tag(takes_context=True)
def rend_reference(context):
    return "Hello, I am tag"
    # try:
    #     pass
    # except ValueError:
    #     msg = '%r tag requires a single argument' % object.contents[0]
    #     raise template.TemplateSyntaxError(msg)
    # return '<a href=\'ololo/olol/\'>'+str(object)+'</a>'

# register.tag('reference_to_edit', rend_reference)

