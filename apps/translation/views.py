from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from translation_manager.manager import Manager
from translation_manager.models import TranslationEntry
from apps.base.utils import has_perms
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.translation.utils import search_function_dict
@csrf_exempt
@staff_member_required(login_url='/nl/account/login')
def index_view(request):
    has_perms(request, ["translation.change_translationentry"], None, 'overviewtranslation')
    page = request.GET.get('page', 1)
    translationEntries = TranslationEntry.objects.filter()
    entries = {}

    key = request.GET.get('key', None)
    nl = request.GET.get('nl', None)
    en = request.GET.get('en', None)

    for entry in translationEntries:
        if entry.original in entries:
            temp = entries[entry.original]
            temp.update({entry.language: {'translation': entry.translation, 'pk': entry.pk}})
            entries.update({entry.original: temp})
        else:
            entries[entry.original] = {entry.language: {'translation': entry.translation, 'pk': entry.pk}}
    entries = search_function_dict(entries, key, nl, en)
    entries = tuple(entries.items())
    paginator = Paginator(entries, 25)

    try:
        translations = paginator.page(page)
    except PageNotAnInteger:
        translations = paginator.page(1)
    except EmptyPage:
        translations = paginator.page(paginator.num_pages)

    return render(request, 'translations/index.html', {
        'entries': translations,
        'searchkey': key,
        'searchnl': nl,
        'searchen': en
    })

@csrf_exempt
@staff_member_required(login_url='/nl/account/login')
def update_translation(request):
    if request.method == "POST":
        TranslationEntry.objects.update_or_create(
            id=int(request.POST.get('entry_id')),
            defaults={
                'translation': request.POST.get('value'),
                'lang': request.POST.get('lang')
            }
        )
        messages.add_message(request, messages.SUCCESS, _('De vertaling is succesvol geupdate!'))
        translation_manager = Manager()
        for lang in settings.LANGUAGES:
            translation_manager.update_po_from_db(lang=lang[0])
        return HttpResponse()

