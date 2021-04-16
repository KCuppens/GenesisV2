from django.utils.translation import gettext_lazy as _
from apps.pages.models import Page
from apps.user.models import User
import xlsxwriter
import io
from django.http import HttpResponse
import datetime
now = datetime.datetime.now()
import pandas
class Import:

    def get_all_models():
        return [
            ('Page', _('Pagina')),
            ('User', _('Gebruiker'))
        ]  

    def get_required_fields(model):
        return {
            'Page': ['page_title'],
            'User': ['email', 'first_name', 'last_name']
        }[model]

    def get_unique_fields(model):
        return {
            'Page': ['slug'],
            'User': ['email']
        }[model]

    def check_unique_fields(link, orig, model):
        unique =  Import.get_unique_fields(model)
        if link in unique:
            param = orig + '=' + str(link)
            qs = eval(model).objects.filter().first()
            if qs:
                return False
        return True

    def get_all_fields_by_model(model, nullable = False):
        field_list = []
        exclude_list = ['canvas', 'slug', 'edited_by', 'deletable','author','page_title','menu_title']
        for field in eval(model)._meta.fields:
            if not nullable and not field.name in exclude_list:
                field_list.append(field)
            elif nullable and field.null:
                field_list.append(field)
        return field_list

    def get_headers_excel(file):
        excel = pandas.read_excel(file, header=0)
        return excel.head()

    def get_excel_without_header(file, header=0):
        excel = pandas.read_excel(file, header=0)
        return excel

    def get_first_data_row_excel(file):
        excel = pandas.read_excel(file, nrows=1, skiprows=[0])
        return excel

    def get_data_array(file):
        counter = 0
        values = Import.get_first_data_row_excel(file)
        data_list = []
        for data in Import.get_headers_excel(file):
            data_list[data] = values[counter]
            count += 1
        return data_list

    def model_importer(excel, value, links, model):
        nr_rows = len(excel.index)
        nr_cols = len(excel.columns)
        created_models = []
        skip_not_unique = False
        for row in range(nr_rows):
            param = ''
            for col in range(nr_cols):
                val = excel.iloc[row, col].replace('X','True')
                link = links[col].replace('_nl', '')
                link = link.replace('_fr', '')
                link = link.replace('_en', '')
                unique = Import.check_unique_fields(link, links[col], model)
                if unique:
                    skip_not_unique = True
                if isinstance(val, str):
                    param += links[col] + '=' + '"' + val + '"'
                else:
                    param += links[col] + '=' + val
                if not col == (nr_cols - 1):
                    param += ','
            if not skip_not_unique:
                object = eval(model + '(' + param + ')')
                object.save()
                created_models.append(object)
        return created_models



        




    