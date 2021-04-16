from modeltranslation.translator import translator, TranslationOptions
from .models import Module, ModulePage, Tab

class ModuleTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')

class ModulePageTranslationOptions(TranslationOptions):
    fields = ('name',)

class TabTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')

translator.register(Module, ModuleTranslationOptions)
translator.register(ModulePage, ModulePageTranslationOptions)
translator.register(Tab, TabTranslationOptions)