from django.contrib import admin

from .models import (
    FieldChoice,
    FieldType,
    Form,
    FormField,
    FormFieldChoiceMembership,
    FormFieldGroup,
    FormFieldResponse,
    FormResponse,
)

# Register your models here.
admin.site.register(FieldChoice)
admin.site.register(FieldType)
admin.site.register(Form)
admin.site.register(FormField)
admin.site.register(FormFieldChoiceMembership)
admin.site.register(FormFieldGroup)
admin.site.register(FormFieldResponse)
admin.site.register(FormResponse)
