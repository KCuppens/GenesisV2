from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from translation_manager.manager import Manager
from translation_manager.models import TranslationEntry
from apps.base.utils import has_perms
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.translation.utils import search_function_dict, get_media_path
from django.conf import settings
import xlsxwriter
import io
import pandas
import datetime 
from apps.translation.forms import ImportFileForm
now = datetime.datetime.now()

@csrf_exempt
@staff_member_required(login_url=reverse_lazy('login'))
def index_view(request):
    has_perms(request, ["translation.view_translationentry"], None, 'dashboard')
    page = request.GET.get('page', 1)
    translationEntries = TranslationEntry.objects.filter()
    entries = {}

    key = request.GET.get('key', None)
    nl = request.GET.get('nl', None)
    en = request.GET.get('en', None)
    fr = request.GET.get('fr', None)

    for entry in translationEntries:
        if entry.original in entries:
            temp = entries[entry.original]
            temp.update({entry.language: {'translation': entry.translation, 'pk': entry.pk}})
            entries.update({entry.original: temp})
        else:
            entries[entry.original] = {entry.language: {'translation': entry.translation, 'pk': entry.pk}}
    entries = search_function_dict(entries, key, nl, en, fr)
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
        'searchen': en,
        'searchfr': fr
    })

@csrf_exempt
@staff_member_required(login_url=reverse_lazy('login'))

def update_translation(request):
    has_perms(request, ["translation.change_translationentry"], None, 'index-translation')
    if request.method == "POST":
        TranslationEntry.objects.update_or_create(
            id=int(request.POST.get('entry_id')),
            defaults={
                'translation': request.POST.get('value'),
                'lang': request.POST.get('lang')
            }
        )
        translation_manager = Manager()
        for lang in settings.LANGUAGES:
            translation_manager.update_po_from_db(lang=lang[0])
        return HttpResponse()

def import_translation(request):
    has_perms(request, ["translation.change_translationentry"], None, 'index-translation')
    if request.method == 'POST':
        form = ImportFileForm(request.POST or request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.SUCCESS, _('The file has been succesfully imported!'))
            return redirect('index-translation')
    else:
        form = ImportFileForm()

    return render(request, 'translations/file.html', {
        'form': form,
    })

def import_file_translation(request):
    has_perms(request, ["translation.change_translationentry"], None, 'index-translation')
    file = request.POST.get('file', False)
    if file:
        path = get_media_path(file)
        excel = pandas.read_excel(path, header=0)

        nr_rows = len(excel.index)
        nr_cols = len(excel.columns)
        for row in range(nr_rows):
            for col in range(nr_cols):
                val = excel.iloc[row, col]
                val = str(val).replace('nan', '')
                skip_row = False
                if col == 0:
                    key_nl = TranslationEntry.objects.filter(original=val, language="nl").first()
                    key_fr = TranslationEntry.objects.filter(original=val, language="fr").first()
                    key_en = TranslationEntry.objects.filter(original=val, language="en").first()
                    if not key_nl and not key_fr and not key_en:
                        skip_row = True                     
                elif col == 1 and not skip_row and key_en:
                    key_en.translation = val
                    key_en.save()
                elif col == 2 and not skip_row and key_nl:
                    key_nl.translation = val
                    key_nl.save()
                elif col == 3 and not skip_row and key_fr:
                    key_fr.translation = val
                    key_fr.save()
        return redirect('index-translation')
    else:
        return redirect('import-translation')


def export_translation(request): 
    has_perms(request, ["translation.view_translationentry"], None, 'index-translation')
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI']
    entries = {}
    output = io.BytesIO()
        
    workbook = xlsxwriter.Workbook(output, {'remove_timezone': True} )
    worksheet =  workbook.add_worksheet()
    row = 1

    translationEntries = TranslationEntry.objects.filter()
    for entry in translationEntries:
        if entry.original in entries:
            temp = entries[entry.original]
            temp.update({entry.language: {'translation': entry.translation, 'pk': entry.pk}})
            entries.update({entry.original: temp})
        else:
            entries[entry.original] = {entry.language: {'translation': entry.translation, 'pk': entry.pk}}

    headers = [_('Key'), _('English'), _('Dutch'), _('French')]
    counter = 0
    for header in headers:
        worksheet.write(letters[counter] + str(row), str(header))
        counter += 1

    row += 1
    for key, value in entries.items():
        worksheet.write(letters[0] + str(row), key)
        if 'en' in value:
            worksheet.write(letters[1] + str(row), value['en']['translation'])
        if 'nl' in value:
            worksheet.write(letters[2] + str(row), value['nl']['translation'])
        if 'fr' in value:
            worksheet.write(letters[3] + str(row), value['fr']['translation'])
        row += 1

    workbook.close()
    output.seek(0)

    filename = 'export_translation_' + now.strftime("%H:%M:%S") + '.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response