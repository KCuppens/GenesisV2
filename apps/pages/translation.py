from modeltranslation.translator import translator, TranslationOptions
from .models import Page, PageBlock

class PageTranslationOptions(TranslationOptions):
    fields = ('page_title', 'menu_title', 'slug')

class PageBlockTranslationOptions(TranslationOptions):
    fields = ('title','content','subtitle','url','url_text')

translator.register(Page, PageTranslationOptions)
translator.register(PageBlock, PageBlockTranslationOptions)