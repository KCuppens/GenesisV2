from apps.pages.models import Page
from django import forms, template
register = template.Library()
from apps.dashboard.dashboard import Dashboard

@register.simple_tag
def render_dashboard_method(method, sort, order, param1):
    dashboard = Dashboard()
    if method == 'count_pages':
        return dashboard.count_pages()
    elif method == 'latest_pages':
        return dashboard.latest_pages(param1)
    elif method == 'count_files_by_type':
        return dashboard.count_files_by_type(param1)
    elif method == 'count_files':
        return dashboard.count_files()
    elif method == 'count_dirs':
        return dashboard.count_dirs()
    elif method == 'count_filemanager_size':
        return dashboard.count_filemanager_size(param1)
    elif method == 'latest_history':
        return dashboard.latest_history(param1, order, sort)
    elif method == 'latest_users':
        return dashboard.latest_users(param1)
    elif method == 'count_users':
        return dashboard.count_users()
        

