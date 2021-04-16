from modeltranslation.translator import translator, TranslationOptions
from .models import Block, BlockCategory

class BlockTranslationOptions(TranslationOptions):
    fields = ('name','slug')

class BlockCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'slug')

translator.register(Block, BlockTranslationOptions)
translator.register(BlockCategory, BlockCategoryTranslationOptions)