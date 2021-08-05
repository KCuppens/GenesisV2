from django.db import connection
from django.shortcuts import render
from apps.base.middleware import redirect
from apps.base.errors import PermissionDenied
from django.utils.translation import ugettext as _
from django.contrib import messages


def check_tables(table_name):
    with connection.cursor() as cursor:
        stmt = "SHOW TABLES LIKE '%s' "% ('%'+str(table_name)+'%')
        cursor.execute(stmt)
        result = cursor.fetchone()  
    return result


def has_perms(request, permissions, template, redirect_url = None, raise_exception=False):
    current_url = request.resolver_match.url_name
    print('current_url: ', current_url)
    if isinstance(permissions, str):
        perms = (permissions,)
    else:
        perms = permissions

    # Check if user is superuser
    if request.user.is_superuser:
        return True

    # First check if the user has the permission (even anon users)
    print(request.user.user_permissions.all())
    print(request.user.groups.all())
    if request.user.has_perms(perms):
        return True
    # In case the 403 handler should be called raise the exception
    if raise_exception:
        raise PermissionDenied
    
    if template:
        return render(request, template, {
                'permission_denied': True,
            })
    elif redirect_url == current_url:
        # preveting the infinite loop if view redirects to itself
        msg = _(f'You don\'t have {perms} permission for this operation')
        raise PermissionDenied(msg)
    elif redirect_url:
        messages.add_message(request, messages.WARNING, _(f'You don\'t have {perms} permission for this operation'))
        return redirect(redirect_url)

def generate_perma_url(locale, model, id):
    return '/' + locale + '/' + 'perma/url/' + model.lower()  + '/' + str(id)