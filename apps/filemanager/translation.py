from modeltranslation.translator import translator, TranslationOptions
from .models import Directory, Media

class DirectoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug', 'summary')

class MediaTranslationOptions(TranslationOptions):
    fields = ('name', 'copyright', 'summary', 'slug', 'keywords', 'alt', 'metadata')


translator.register(Directory, DirectoryTranslationOptions)
translator.register(Media, MediaTranslationOptions)