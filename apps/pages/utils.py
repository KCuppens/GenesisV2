from apps.pages.models import Page
from django.utils.text import slugify

def check_if_homepage_exists(page):
    if Page.objects.filter(is_homepage=True, date_deleted=None).exclude(id=page.id).first():
        return True
    return False

def generate_slug(page):
    if page.url_type == Page.URL_TYPE_GENERATED:
        if page.is_homepage:
            page.slug = ''
        else:
            page.slug = slugify(page.page_title)
        page.save()
    


def generate_full_slug(current_page):
    full_slug = ''
    slug = current_page.slug
    if slug:
        page = current_page
        while page.parent:
            page = page.parent
            full_slug += page.slug + '/'
        full_slug += slug
        
        current_page.full_slug =  full_slug
        current_page.save()
        return full_slug
    
