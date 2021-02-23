from apps.modules.models import Tab

def get_topnav(request):
    return {
        'tabs': Tab.objects.filter(date_deleted=None, active=True)
    }