from modeltranslation.translator import translator, TranslationOptions
from apps.news.models import Article

class ArticleTranslationOptions(TranslationOptions):
    fields=('title', 'slug', 'summary', 'content', 'meta_title', 'meta_description', 'meta_keywords','active')

translator.register(Article, ArticleTranslationOptions)