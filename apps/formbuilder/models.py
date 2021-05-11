from django.db import models
from apps.base.models import BaseModel, AdminModel, SortableModel, BaseRevision, BaseVersion
from apps.mail.models import MailTemplate
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
# Create your models here.

class Form(BaseModel, AdminModel):
    SUCCESS_TYPE_MESSAGE = 'message'
    SUCCESS_TYPE_ACTION = 'action'
    SUCCESS_TYPE_REDIRECT = 'redirect'

    SUCCESS_TYPES = [
        (SUCCESS_TYPE_MESSAGE, _('Message')),
        (SUCCESS_TYPE_ACTION, _('Action')),
        (SUCCESS_TYPE_REDIRECT, _('Redirect'))
    ]

    name = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')
    success_type = models.CharField(max_length=255, null=True, blank=True, choices=SUCCESS_TYPES, default=SUCCESS_TYPE_MESSAGE)
    success_action = models.CharField(max_length=255, null=True, blank=True)
    success_url = models.CharField(max_length=255, null=True, blank=True)
    success_message = models.TextField(null=True, blank=True)
    send_mail = models.BooleanField(default=False) 
    mail_recipient_name = models.CharField(max_length=255, null=True, blank=True)
    mail_recipient_email = models.CharField(max_length=255, null=True, blank=True)
    mail_admin = models.ForeignKey(MailTemplate, on_delete=models.CASCADE, related_name="mail_admin", blank=True, null=True)
    mail_sender_name = models.CharField(max_length=255, null=True, blank=True)
    mail_sender_email = models.CharField(max_length=255, null=True, blank=True)
    mail_sender_visitor = models.BooleanField(default=False) 
    mail_visitor = models.ForeignKey(MailTemplate, on_delete=models.CASCADE, related_name="mail_visitor", blank=True, null=True)
    mail_visitor_sender_name = models.CharField(max_length=255, null=True, blank=True)
    mail_visitor_sender_email = models.CharField(max_length=255, null=True, blank=True)
    store_results = models.BooleanField(default=False) 
    pages = models.ManyToManyField('formpage', blank=True)

    def __str__(self):
        return self.name 

class FormPage(models.Model):
    elements = models.ManyToManyField('formelement', blank=True) 
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')

class FormElement(SortableModel):
    TYPE_TEXT_FIELD = 'text_field'
    TYPE_TEXT_AREA_FIELD = 'textarea_field'
    TYPE_CHECKBOX_FIELD = 'checkbox_field'
    TYPE_DATE_FIELD = 'date_field'
    TYPE_DATETIME_FIELD = 'datetime_field'
    TYPE_DECIMAL_FIELD = 'decimal_field'
    TYPE_DURATION_FIELD = 'duration_field'
    TYPE_EMAIL_FIELD = 'email_field'
    TYPE_FILE_FIELD = 'file_field'
    TYPE_SUBMIT_BUTTON = 'submit_button'
    TYPE_IMAGE_FIELD = 'image_field'
    TYPE_HIDDEN_FIELD = 'hidden_field'
    TYPE_MULTI_RADIO_FIELD = 'multi_radio_field'
    TYPE_RANGE_FIELD = 'range_field'
    TYPE_SELECT_FIELD = 'select_field'
    #TYPE_MODEL_SELECT_FIELD = 'model_select_field'
    #TYPE_SELECT_MULTIPLE_FIELD = 'select_multiple_field'
    #TYPE_MODEL_SELECT_MULTIPLE_FIELD = 'model_select_multiple_field'
    TYPE_SLIDER_FIELD = 'slider_field'
    TYPE_TIME_FIELD = 'time_field'
    TYPE_URL_FIELD = 'url_field'

    TYPE_CONTENT_IMAGE = 'content_image'
    TYPE_CONTENT_TEXT = 'content_text'
    TYPE_CONTENT_VIDEO = 'content_video'

    TYPE_SECURITY_CAPTCHA = 'security_captcha'
    TYPE_SECURITY_HONEYPOT = 'security_honeypot'

    GET_FIELDS = [
        (TYPE_SUBMIT_BUTTON, _('Knop')),
        (TYPE_TEXT_FIELD, _('Tekstveld')),
        (TYPE_TEXT_AREA_FIELD, _('Groot tekstveld')),
        (TYPE_CHECKBOX_FIELD, _('Checkboxveld')),
        (TYPE_DATE_FIELD, _('Datumveld')),
        (TYPE_DATETIME_FIELD, _('Datum- en tijdveld')),
        (TYPE_DECIMAL_FIELD, _('Decimalveld')),
        (TYPE_DURATION_FIELD, _('Duratieveld')),
        (TYPE_EMAIL_FIELD, _('Emailveld')),
        (TYPE_FILE_FIELD, _('Bestandsveld')),
        (TYPE_IMAGE_FIELD, _('Afbeeldingsveld')),
        (TYPE_HIDDEN_FIELD, _('Verborgenveld')),
        (TYPE_MULTI_RADIO_FIELD, _('Multi radioveld')),
        (TYPE_RANGE_FIELD, _('Rangeveld')),
        (TYPE_SELECT_FIELD, _('Selectveld')),
        #(TYPE_MODEL_SELECT_FIELD, _('Model selectveld')),
        (TYPE_SLIDER_FIELD, _('Sliderveld')),
        (TYPE_TIME_FIELD, _('Tijdsveld')),
        (TYPE_URL_FIELD, _('URL veld')),
    ]

    GET_CONTENT_FIELDS = [
        (TYPE_CONTENT_IMAGE, _('Inhoudsafbeelding')),
        (TYPE_CONTENT_TEXT, _('Tekstinhoud')),
        (TYPE_CONTENT_VIDEO, _('Video inhoud')),
    ]

    GET_TYPES = [
        (TYPE_SUBMIT_BUTTON, _('Knop')),
        (TYPE_TEXT_FIELD, _('Tekstveld')),
        (TYPE_TEXT_AREA_FIELD, _('Groot tekstveld')),
        (TYPE_CHECKBOX_FIELD, _('Checkboxveld')),
        (TYPE_DATE_FIELD, _('Datumveld')),
        (TYPE_DATETIME_FIELD, _('Datum- en tijdveld')),
        (TYPE_DECIMAL_FIELD, _('Decimalveld')),
        (TYPE_DURATION_FIELD, _('Duratieveld')),
        (TYPE_EMAIL_FIELD, _('Emailveld')),
        (TYPE_FILE_FIELD, _('Bestandsveld')),
        (TYPE_IMAGE_FIELD, _('Afbeeldingsveld')),
        (TYPE_HIDDEN_FIELD, _('Verborgenveld')),
        (TYPE_MULTI_RADIO_FIELD, _('Multi radioveld')),
        (TYPE_RANGE_FIELD, _('Rangeveld')),
        (TYPE_SELECT_FIELD, _('Selectveld')),
        #(TYPE_MODEL_SELECT_FIELD, _('Model selectveld')),
        (TYPE_SLIDER_FIELD, _('Sliderveld')),
        (TYPE_TIME_FIELD, _('Tijdsveld')),
        (TYPE_URL_FIELD, _('URL veld')),
        (TYPE_CONTENT_IMAGE, _('Inhoudsafbeelding')),
        (TYPE_CONTENT_TEXT, _('Tekstinhoud')),
        (TYPE_CONTENT_VIDEO, _('Video inhoud')),
        (TYPE_SECURITY_CAPTCHA, _('Captchaveld')),
        (TYPE_SECURITY_HONEYPOT, _('Honeypotveld'))
    ]
    
    COL_SIZE_FULL = 'full'
    COL_SIZE_HALF = 'half'
    COL_SIZE_QUARTER = 'quarter'

    GET_COL_SIZES = [
        (COL_SIZE_FULL, _('Volledige kolom')),
        (COL_SIZE_HALF, _('Halve kolom')),
        (COL_SIZE_QUARTER, _('Kwart kolom'))
    ]

    label = models.CharField(max_length=255, null=True, blank=True) 
    name = models.CharField(max_length=255, null=True, blank=True) 
    placeholder = models.CharField(max_length=255, null=True, blank=True)
    form_class = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True, choices=GET_TYPES, default=TYPE_TEXT_FIELD) 
    select_type = models.CharField(max_length=255, null=True, blank=True)
    select_multiple = models.BooleanField(default=False) 
    min_date = models.DateField(null=True, blank=True)
    max_date = models.DateField(null=True, blank=True)
    is_checked = models.BooleanField(default=False)  
    required = models.BooleanField(default=False)  
    image = models.CharField(max_length=255, null=True, blank=True)
    video = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    default = models.CharField(max_length=255, null=True, blank=True) 
    options = models.ManyToManyField('formelementoption', blank=True)
    col_size = models.CharField(max_length=255, default=COL_SIZE_FULL, choices=GET_COL_SIZES, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']

class FormElementOption(SortableModel):
    label = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True) 
    value = models.CharField(max_length=255, null=True, blank=True) 
    condition_value = models.CharField(max_length=255, null=True, blank=True) 
    is_checked = models.BooleanField(default=False)  

    class Meta:
        ordering = ['position']

class FormResult(BaseModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    entries = models.ManyToManyField('formresultfield', blank=True)

class FormResultField(models.Model):
    value = models.TextField(null=True, blank=True)
    field = models.ForeignKey(FormElement, on_delete=models.CASCADE) 
    field_type = models.TextField(null=True, blank=True) 
    page = models.CharField(max_length=255, null=True, blank=True) 


class FormRevision(BaseRevision):
    current_instance = models.OneToOneField(Form, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, default="form")


class FormVersion(BaseVersion):
    revision = models.ForeignKey(FormRevision, on_delete=models.CASCADE, related_name="versions")

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        try:
            formversion = FormVersion.objects.get(id=self.id)
            for version in formversion.revision.versions.all().exclude(id=self.id):
                if self.is_current:
                    version.is_current = False
                    version.save()
        except:
            for version in FormVersion.objects.exclude(id=self.id):
                version.is_current = False
                version.save()
        super().save(*args, **kwargs)

