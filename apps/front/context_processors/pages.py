from apps.pages.models import Page
def get_menu(request):
    return {
        'pages': Page.objects.filter(active=True, date_deleted=None, in_main_menu=True),
        'topnav': Page.objects.filter(active=True, date_deleted=None, in_topnav_menu=True),
        'quicklinks': Page.objects.filter(active=True, date_deleted=None, in_quicklinks_menu=True)
    }

