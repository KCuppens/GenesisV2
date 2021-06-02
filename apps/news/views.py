from apps.pages.models import DetailPage
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, resolve_url
from apps.conf.utils import get_config
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from apps.base.utils import has_perms
from apps.news.models import Article , NewsRevision, NewsVersion
from apps.news.forms import ArticleForm
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import OrderedDict
from django.db import transaction
import json
from datetime import datetime
from apps.pages.models import DetailPage


@staff_member_required(login_url=reverse_lazy('login'))
def overview_article(request):
    articles = Article.objects.filter(date_deleted=None)
    has_perms(request, ["news.view_article"], None, 'overviewarticle')
    for article in articles:
        try:
            newsrevision = NewsRevision.objects.get(current_instance=article)
            versions = newsrevision.versions.all()
            article.has_versions = bool(versions)
        except:
            continue
    
    return render(request,'news/index.html', {"articles":articles})


@transaction.atomic
@staff_member_required(login_url=reverse_lazy('login'))
def add_article(request):
    has_perms(request, ["news.add_article"], None, 'overviewarticle')
    if request.method == 'POST':
        # import pdb;pdb.set_trace()
        form = ArticleForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The article has been succesfully added!'))

            return redirect('overviewarticle')
    else:
        form = ArticleForm()

    return render(request, 'news/add.html', {
        'form': form,
    })

@transaction.atomic
@staff_member_required(login_url=reverse_lazy('login'))
def edit_article(request, pk):
    has_perms(request, ["news.change_article"], None, 'overviewarticle')
    instance = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST or request.FILES,instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, _('The article has been succesfully changed!'))

            return redirect('overviewarticle')
    else:
        form = ArticleForm(instance=instance)
    return render(request, 'news/edit.html', {
        'form': form,
        'article':instance
    })

@staff_member_required(login_url=reverse_lazy('login'))
def delete_ajax_article_modal(request):
    data = {}
    id = request.POST.get('id', False)
    article = Article.objects.get(id=id)
    if article:
        context = {
            'article': article
        }
        data = {
            'template': render_to_string('news/__partials/modal.html', context=context, request=request)
        }
    return JsonResponse(data)


@staff_member_required(login_url=reverse_lazy('login'))
def overview_reversion(request):
    articles = Article.objects.filter(date_deleted__isnull=False)
    return render(request,'news/reversion-overview-index.html', {"articles":articles})

@staff_member_required(login_url=reverse_lazy('login'))
def revert_article(request, pk):
    try:
        article = Article.objects.get(id=pk)
        article.date_deleted = None
        article.save()
        messages.add_message(request, messages.SUCCESS, _('The Article has been succesfully reverted!'))
    except:
        messages.add_message(request, messages.WARNING, _('No such article is available!'))
    
    return redirect('overviewreversionarticle')

@staff_member_required(login_url=reverse_lazy('login'))
def get_version_ajax_article_modal(request):
    data = {}
    # import pdb;pdb.set_trace();
    id = request.POST.get('id', False)
    reversion = NewsRevision.objects.get(current_instance=Article.objects.get(id=id))
    article_version = NewsVersion.objects.filter(revision=reversion).order_by("date_created")
    if article_version:
        context = {
            'article_version': article_version
        }
        data = {
            'template': render_to_string('news/__partials/version_modal.html', context=context, request=request)
        }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def get_delete_version_ajax_article_modal(request):
    data = {}
    # import pdb;pdb.set_trace();
    id = request.POST.get('id', False)
    try:
        version = NewsVersion.objects.get(id=id)
    except:
        version = None
    if version:
        context = {
            'version': version
        }
        data = {
            'template': render_to_string('news/__partials/delete_version_modal.html', context=context, request=request)
        }
    return JsonResponse(data)

@staff_member_required(login_url=reverse_lazy('login'))
def select_version(request, pk):
    # import pdb;pdb.set_trace();
    article_version = NewsVersion.objects.get(id=pk)
    # article_version.is_current = True
    # article_version.save()

    article_version_dict = json.loads(article_version.serialized_instance)
    article = NewsRevision.objects.get(versions__id=pk).current_instance
    for attr, value in article_version_dict.items():
        setattr(article, attr, value)
    article.not_new_object=1
    article.save()
    # messages.add_message(request, messages.SUCCESS, _('De versie is succesvol verwijderd'))
    return redirect('overviewarticle')

@staff_member_required(login_url=reverse_lazy('login'))
def delete_version(request, pk):
    # import pdb;pdb.set_trace();
    article_version = NewsVersion.objects.get(id=pk)
    if article_version.is_current:
        # redirect if is_current=True
        messages.add_message(request, messages.WARNING, _('U kunt de momenteel geselecteerde versie niet verwijderen!'))
        return redirect('overviewarticle')
    article_version.delete()
    messages.add_message(request, messages.SUCCESS, _('De versie is succesvol verwijderd'))
    return redirect('overviewarticle')

@staff_member_required(login_url=reverse_lazy('login'))
def add_version_comment(request, pk):
    # import pdb;pdb.set_trace();
    article_version = NewsVersion.objects.get(id=pk)
    comment = request.POST.get('comment')
    if comment and comment != article_version.comment:
        article_version.comment = comment
        article_version.save()
        messages.add_message(request, messages.SUCCESS, _('De opmerking is succesvol opgeslagen!'))
    return redirect('overviewarticle')


@staff_member_required(login_url=reverse_lazy('login'))
def toggle_article_activation_view(request, pk):
    has_perms(request, ["news.change_article"], None, 'overviewarticle')

    item = Article.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de article is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewarticle')

@transaction.atomic
@staff_member_required(login_url=reverse_lazy('login'))
def delete_article(request,pk):
    has_perms(request, ["news.delete_article"], None, 'overviewarticle')
    instance = Article.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    detailpage = DetailPage.objects.filter(model='Article', object_id=instance.id, default=False).first()
    if detailpage:
        detailpage.delete()
    messages.add_message(request, messages.SUCCESS, _('The article has been succesfully deleted!'))
    return redirect('overviewarticle')

def get_articles(request):
    page = request.POST.get('page', 1)
    sort_method = request.POST.get('sort_method', False)
    sort_order = request.POST.get('sort_order', False)
    pagination = request.POST.get('pagination', 6)
    articles_list = Article.objects.get_actives(sort_method, sort_order)
    results_per_page = int(pagination)
    paginator = Paginator(articles_list, results_per_page)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(2)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    context = {
        'articles': articles,
        'has_next': articles.has_next()
    }
    data = {
        'template': render_to_string('news/__partials/overview.html', context=context, request=request), 
    }
    return JsonResponse(data)

def get_article_detail(request):
    article = request.POST.get('article')

    article_obj = Article.objects.filter(id=article).first()

    context = {
        'item': article_obj,
    }
    data = {
        'template': render_to_string('news/__partials/detail.html', context=context, request=request), 
    }
    return JsonResponse(data)



