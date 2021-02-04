from django.db import models
from apps.base.models import BaseModel, AdminModel, SeoModel, SortableModel
# Create your models here.
class Page(BaseModel, AdminModel, SeoModel, SortableModel):
    pass 
