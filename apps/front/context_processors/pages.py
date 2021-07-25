from apps.pages.models import Page
def get_menu(request):
    slug = request.resolver_match.kwargs.get('slug')
    current_page = Page.objects.filter(full_slug=slug).first()
    return {
        'pages': Page.objects.filter(active=True, date_deleted=None, in_main_menu=True).order_by('position'),
        'topnav': Page.objects.filter(active=True, date_deleted=None, in_topnav_menu=True).order_by('position'),
        'quicklinks': Page.objects.filter(active=True, date_deleted=None, in_quicklinks_menu=True).order_by('position'),
        'current_page': current_page
    }

