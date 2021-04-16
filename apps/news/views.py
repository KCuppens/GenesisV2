from django.shortcuts import render,get_object_or_404,redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.
from django.contrib import messages
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, resolve_url
from apps.conf.utils import get_config
from django.views.generic import View
from django.contrib.admin.views.decorators import staff_member_required
from apps.base.utils import has_perms
from apps.news.models import Article
from apps.news.forms import ArticleForm
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@staff_member_required(login_url='/nl/account/login')
def overview_article(request):
    articles = Article.objects.filter(date_deleted=None)
    has_perms(request, ["news.view_article"], None, 'overviewarticle')
    
    return render(request,'news/index.html', {"articles":articles})

@staff_member_required(login_url='/nl/account/login')
def add_article(request):
    has_perms(request, ["news.add_article"], None, 'overviewarticle')
    if request.method == 'POST':
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

@staff_member_required(login_url='/nl/account/login')
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

@staff_member_required(login_url='/nl/account/login')
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

@staff_member_required(login_url='/nl/account/login')
def toggle_article_activation_view(request, pk):
    has_perms(request, ["news.change_article"], None, 'overviewarticle')

    item = Article.objects.get(pk=pk)
    item.active = not item.active
    messages.add_message(request, messages.SUCCESS, _('De status van de article is succesvol aangepast!'))
    item.save()
    
    return redirect('overviewarticle')

        
@staff_member_required(login_url='/nl/account/login')
def delete_article(request,pk):
    has_perms(request, ["news.delete_article"], None, 'overviewarticle')
    instance = Article.objects.get(pk=pk)
    instance.date_deleted = timezone.now()
    instance.save()
    messages.add_message(request, messages.SUCCESS, _('The module has been succesfully deleted!'))
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



