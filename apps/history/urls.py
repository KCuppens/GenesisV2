from django.conf.urls import url
from .views import overview_history
from django.utils.translation import ugettext as _

urlpatterns = [
    url(_('^overview$').strip(),overview_history,name="overviewhistory"),
]