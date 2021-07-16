from django import forms, template
register = template.Library()

@register.simple_tag
def get_group_permission_ids(group):
    print('Group: ', group)
    return [perm.id for perm in group.permissions.all()]