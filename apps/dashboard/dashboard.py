from apps.filemanager.models import Directory, Media
from apps.pages.models import Page 
from apps.user.models import User
from apps.history.models import History
class Dashboard:
    #filemanager
    def count_files_by_type(self, type):
        return Media.objects.filter(type=type, date_deleted=None).count()

    def count_files(self):
        return Media.objects.filter(date_deleted=None).count()

    def count_dirs(self):
        return Directory.objects.filter(date_deleted=None).count()

    def count_filemanager_size(self, type):
        if type:
            return Media.objects.aggregate(num_size=Sum('file_size')).filter(type=type)
        return Media.objects.aggregate(num_size=Sum('file_size'))

    #history
    def latest_history(self, limit, order, sort):
        if limit:
            return History.objects.filter()[:limit]
        elif order and sort:
            if order == 'ASC':
                return History.objects.filter().order_by(sort)
            elif order == 'DESC':
                return History.objects.filter().order_by('-' + sort)
        return History.objects.filter()

    #logs
    #TODO

    #pages
    def latest_pages(self, limit = 3):
        return Page.objects.filter(active=True, date_deleted=None).order_by('-date_published')[:limit]

    def count_pages(self):
        return Page.objects.filter(active=True, date_deleted=None).count()

    #user
    def latest_users(self, limit = 3):
        return User.objects.filter(is_active=True, date_deleted=None).order_by('-date_created')[:limit]

    def count_users(self):
        return User.objects.filter(is_active=True, date_deleted=None).count()