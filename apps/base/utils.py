from django.db import connection

def check_tables(table_name):
    with connection.cursor() as cursor:
        stmt = "SHOW TABLES LIKE '%s' "% ('%'+str(table_name)+'%')
        cursor.execute(stmt)
        result = cursor.fetchone()  
    return result


def has_perms(request, permissions, template, redirect = None, raise_exception=False):
    if isinstance(permissions, str):
        perms = (permissions,)
    else:
        perms = permissions
    # First check if the user has the permission (even anon users)
    if request.user.has_perms(perms):
        return True
    # In case the 403 handler should be called raise the exception
    if raise_exception:
        raise PermissionDenied
    
    if template:
        return render(request, template, {
                'permission_denied': True,
            })
    elif redirect:
        return redirect(redirect)

def generate_perma_url(locale, model, id):
    return '/' + locale + '/' + 'perma/url/' + model.lower()  + '/' + str(id)