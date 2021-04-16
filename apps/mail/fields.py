from django.db.models import TextField
from django.utils.translation import gettext as _ 

from .validators import validate_comma_separated_emails 

class CommaSeparatedEmailField(TextField):
    default_validators = [validate_comma_separated_emails]
    description = _('Comma-separated emails')

    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True 
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'error_messages': {
                'invalid': _('Only comma separated emails are allowed.')
            }
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if isinstance(value, str):
            return value 
        else:
            return ', '.join(map(lambda s: s.strip(), value))

    def to_python(self, value):
        if isinstance(value, str):
            if value == '':
                return [] 
            else:
                return [s.strip() for s in value.split(',')]
        else:
            return value 

    def south_field_triple(self):
        """
        Return a suitable description of this field for South.
        Taken from smiley chris' easy_thumbnails
        """
        from south.modelsinspector import introspector
        field_class = 'django.db.models.fields.TextField'
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)