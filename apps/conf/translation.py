from modeltranslation.translator import translator, TranslationOptions
from .models import Configuration

class ConfigurationTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(Configuration, ConfigurationTranslationOptions)