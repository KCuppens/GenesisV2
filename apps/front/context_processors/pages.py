from apps.pages.models import Page
def get_menu(request):
    if request:
        slug = request.resolver_match.kwargs.get('slug')
        if slug == '':
            current_page = Page.objects.filter(slug=slug, active=True, date_deleted=None).first()
        else:
            current_page = Page.objects.filter(full_slug=slug, active=True, date_deleted=None).first()
        return {
            'pages': Page.objects.filter(active=True, date_deleted=None, in_main_menu=True, parent__isnull=True).order_by('position'),
            'all_pages': Page.objects.filter(active=True, date_deleted=None).order_by('position'),
            'topnav': Page.objects.filter(active=True, date_deleted=None, in_topnav_menu=True).order_by('position'),
            'marked': Page.objects.filter(active=True, date_deleted=None, in_marked_menu=True).order_by('position'),
            'current_page': current_page
        }