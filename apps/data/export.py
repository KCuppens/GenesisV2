from django.utils.translation import gettext_lazy as _
from apps.pages.models import Page
from apps.user.models import User
from apps.formbuilder.models import FormResult
import xlsxwriter
import io
from django.http import HttpResponse
import datetime
now = datetime.datetime.now()

class Export:

    def get_all_models():
        return [
            ('Page', _('Pagina')),
            ('User', _('Gebruiker')),
        ]   

    def get_all_fields_by_model(model):
        field_list = []
        exclude_list = ['canvas', 'slug', 'edited_by', 'deletable','author','page_title','menu_title']
        for field in eval(model)._meta.fields:
            if not field.name in exclude_list:
                field_list.append(field)
        return field_list

    def handle_form(checks, names, model):
        fields = Export.get_all_fields_by_model(model)
        counter = 0
        field_list = []
        for field in fields:
            if len(checks) > counter and checks[counter]:
                if names[counter]:
                    name = names[counter]
                else:
                    name = field.verbose_name
                field_list.append([field.name, name])
            counter += 1
        return field_list

    def get_letter_order():
        return ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI']
    
    def generate_xlsx(fields, model):
        output = io.BytesIO()
        
        workbook = xlsxwriter.Workbook(output, {'remove_timezone': True} )
        worksheet =  workbook.add_worksheet()
        row = 1
        letters = Export.get_letter_order()

        if 'date_deleted' in fields:
            objects = eval(model).objects.all()
        else:
            objects = eval(model).objects.filter(date_deleted=None)

        counter = 0
        for fieldname, fieldtitle in fields:
            worksheet.write(letters[counter] + str(row), str(fieldtitle))
            counter += 1

        row += 1
        for object in objects:
            counter = 0
            for fieldname, fieldtitle in fields:
                if fieldname:
                    if str(getattr(object, fieldname)) == "True":
                        worksheet.write(letters[counter] + str(row), "Yes")
                    elif str(getattr(object, fieldname)) == "False":
                        worksheet.write(letters[counter] + str(row), "No")
                    elif not str(getattr(object, fieldname)) == "None":
                        worksheet.write(letters[counter] + str(row), str(getattr(object, fieldname)))
                    else:
                        worksheet.write(letters[counter] + str(row), "")

                counter += 1
            row += 1

        workbook.close()
        output.seek(0)

        filename = 'export_' + model.lower() + '_' + now.strftime("%H:%M:%S") + '.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response